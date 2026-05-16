"""Celery tasks for AI features."""

import json
from datetime import datetime, timezone

from celery_app import celery_app
from core.database import db
from core.logging import setup_logging
from flask import Flask


def _get_app() -> Flask:
    from app import create_app
    return create_app()


if celery_app is not None:

    @celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
    def generate_weekly_reports(self):
        app = _get_app()
        with app.app_context():
            from features.organizations.models import Organization
            from features.tasks.models import Task
            from features.ai.services.reports import generate_report

            orgs = Organization.query.all()
            for org in orgs:
                tasks = Task.query.filter_by(organization_id=org.id).all()
                if not tasks:
                    continue
                summary = f"Total: {len(tasks)}, "
                summary += f"Done: {sum(1 for t in tasks if t.status == 'done')}, "
                summary += f"In Progress: {sum(1 for t in tasks if t.status == 'in_progress')}"
                try:
                    result = generate_report(org.name, summary, "weekly")
                    from features.ai.models import AIInteraction
                    log = AIInteraction(
                        feature="report",
                        prompt=summary,
                        response=json.dumps(result),
                        model=result.get("model", ""),
                        tokens_used=result.get("tokens", 0),
                        latency_ms=result.get("latency_ms", 0),
                    )
                    db.session.add(log)
                    db.session.commit()
                except Exception as exc:
                    self.retry(exc=exc)
