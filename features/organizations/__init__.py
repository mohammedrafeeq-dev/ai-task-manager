from flask import Blueprint

org_bp = Blueprint("organizations", __name__, template_folder="../../templates/organizations")

from features.organizations import routes
