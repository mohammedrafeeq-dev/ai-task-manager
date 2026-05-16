"""Streaming AI chat assistant for task management."""

from typing import Generator
from openai import OpenAI

from config import Config


def chat_stream(messages: list[dict]) -> Generator[str, None, None]:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful task management assistant. "
            "You help users manage their tasks, suggest priorities, "
            "and answer questions about their workflow. "
            "Be concise and practical."
        ),
    }
    full_messages = [system_msg] + messages
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=full_messages,
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and delta.content:
            yield delta.content
