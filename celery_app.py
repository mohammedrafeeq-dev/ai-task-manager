import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = None

if os.getenv("CELERY_ENABLED", "").lower() == "true":
    celery_app = Celery(
        "ai-task-manager",
        broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    )

if celery_app is not None:
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        beat_schedule={
            "generate-weekly-reports": {
                "task": "features.ai.tasks.generate_weekly_reports",
                "schedule": 604800,
            },
        },
    )
