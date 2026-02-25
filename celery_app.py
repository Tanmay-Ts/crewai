from celery import Celery

celery_app = Celery(
    "financial_analyzer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["worker"],  # 🔥 CRITICAL FIX
)

celery_app.conf.update(
    task_track_started=True,
)