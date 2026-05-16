"""Generate AI-powered task reports."""

import json
import time
from openai import OpenAI

from config import Config


def generate_report(org_name: str, task_summary: str, report_type: str = "weekly") -> dict:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Generate a {report_type} report for {org_name}. "
                    "Return JSON with keys: summary (string), highlights (list of strings), "
                    "recommendations (list of strings), completion_rate (float 0-100). "
                    "Only return valid JSON, no markdown."
                ),
            },
            {"role": "user", "content": f"Task data:\n{task_summary}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    latency = int((time.time() - start) * 1000)
    content = resp.choices[0].message.content
    data = json.loads(content) if content else {}
    return {
        "summary": data.get("summary", ""),
        "highlights": data.get("highlights", []),
        "recommendations": data.get("recommendations", []),
        "completion_rate": data.get("completion_rate", 0),
        "model": resp.model,
        "tokens": resp.usage.total_tokens if resp.usage else 0,
        "latency_ms": latency,
    }
