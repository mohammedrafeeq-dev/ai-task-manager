from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__, template_folder="../../templates/tasks")

from features.tasks import routes
