from flask import Blueprint

ai_bp = Blueprint("ai", __name__, template_folder="../../templates/ai")

from features.ai import routes
