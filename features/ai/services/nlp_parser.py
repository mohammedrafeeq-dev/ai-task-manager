"""Parse natural language into structured task fields using OpenAI."""

import json
import time
from openai import OpenAI

from config import Config


def parse_task_from_nl(text: str) -> dict:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract task information from the user's message. "
                    "Return JSON with keys: title (string), description (string or null), "
                    "priority ('low'|'medium'|'high'|'urgent'), "
                    "due_date (ISO date string or null). "
                    "Only return valid JSON, no markdown."
                ),
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    latency = int((time.time() - start) * 1000)
    content = resp.choices[0].message.content
    data = json.loads(content) if content else {}
    return {
        "title": data.get("title", text),
        "description": data.get("description"),
        "priority": data.get("priority", "medium"),
        "due_date": data.get("due_date"),
        "model": resp.model,
        "tokens": resp.usage.total_tokens if resp.usage else 0,
        "latency_ms": latency,
    }
