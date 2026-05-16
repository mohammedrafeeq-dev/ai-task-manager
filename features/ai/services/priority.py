"""Suggest priority and due_date based on task content."""

import json
import time
from openai import OpenAI

from config import Config


def suggest_priority(title: str, description: str = "") -> dict:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze the task title and description. "
                    "Return JSON with keys: priority ('low'|'medium'|'high'|'urgent'), "
                    "due_date (ISO date string or null), reason (short string). "
                    "Only return valid JSON, no markdown."
                ),
            },
            {
                "role": "user",
                "content": f"Title: {title}\nDescription: {description}",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    latency = int((time.time() - start) * 1000)
    content = resp.choices[0].message.content
    data = json.loads(content) if content else {}
    return {
        "priority": data.get("priority", "medium"),
        "due_date": data.get("due_date"),
        "reason": data.get("reason", ""),
        "model": resp.model,
        "tokens": resp.usage.total_tokens if resp.usage else 0,
        "latency_ms": latency,
    }
