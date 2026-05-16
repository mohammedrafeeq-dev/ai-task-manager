import uuid
from flask import g, request


def add_request_id():
    g.request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:8])
