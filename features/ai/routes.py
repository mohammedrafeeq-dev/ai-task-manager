import json
from flask import Response, render_template, request
from flask_login import current_user, login_required

from core.database import db
from features.ai import ai_bp
from features.ai.models import AIInteraction
from features.ai.services.chat import chat_stream
from features.ai.services.nlp_parser import parse_task_from_nl
from features.ai.services.priority import suggest_priority


@ai_bp.route("/chat")
@login_required
def chat():
    return render_template("ai/chat.html")


@ai_bp.route("/chat/send", methods=["POST"])
@login_required
def chat_send():
    message = request.form.get("message", "")
    if not message:
        return "No message", 400

    def generate():
        history = [{"role": "user", "content": message}]
        yield f'<div class="chat-msg user-msg mb-2"><strong>You:</strong> {message}</div>'
        yield '<div class="chat-msg ai-msg mb-2"><strong>AI:</strong> '
        full = ""
        for chunk in chat_stream(history):
            full += chunk
            yield chunk
        yield "</div>"
        AIInteraction(
            user_id=current_user.id,
            feature="chat",
            prompt=message,
            response=full,
            model="gpt-4o",
        )
        db.session.commit()

    return Response(generate(), mimetype="text/html")


@ai_bp.route("/parse", methods=["POST"])
@login_required
def parse():
    text = request.form.get("text", "")
    if not text:
        return {"error": "No text"}, 400
    result = parse_task_from_nl(text)
    AIInteraction(
        user_id=current_user.id,
        feature="parse",
        prompt=text,
        response=json.dumps(result),
        model=result.get("model", ""),
        tokens_used=result.get("tokens", 0),
        latency_ms=result.get("latency_ms", 0),
    )
    db.session.commit()
    return result


@ai_bp.route("/suggest-priority", methods=["POST"])
@login_required
def suggest():
    title = request.form.get("title", "")
    description = request.form.get("description", "")
    result = suggest_priority(title, description)
    AIInteraction(
        user_id=current_user.id,
        feature="priority",
        prompt=f"{title}\n{description}",
        response=json.dumps(result),
        model=result.get("model", ""),
        tokens_used=result.get("tokens", 0),
        latency_ms=result.get("latency_ms", 0),
    )
    db.session.commit()
    return result
