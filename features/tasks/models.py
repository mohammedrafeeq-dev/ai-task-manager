from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text, Table

from core.database import db
from core.models.mixins import OrganizationMixin, PKMixin, TimestampMixin

task_labels = Table(
    "task_labels",
    db.metadata,
    Column("task_id", String(36), ForeignKey("task.id", ondelete="CASCADE"), primary_key=True),
    Column("task_label_id", String(36), ForeignKey("task_label.id", ondelete="CASCADE"), primary_key=True),
)


class Task(PKMixin, TimestampMixin, OrganizationMixin, db.Model):
    __tablename__ = "task"

    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    status = Column(Enum("todo", "in_progress", "done", "archived", name="task_status"), default="todo", nullable=False)
    priority = Column(Enum("low", "medium", "high", "urgent", name="task_priority"), default="medium", nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_by_id = Column(String(36), ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    assigned_to_id = Column(String(36), ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    labels = db.relationship("TaskLabel", secondary=task_labels, back_populates="tasks")


class TaskComment(PKMixin, TimestampMixin, db.Model):
    __tablename__ = "task_comment"

    task_id = Column(String(36), ForeignKey("task.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    content = Column(Text, nullable=False)


class TaskLabel(PKMixin, OrganizationMixin, db.Model):
    __tablename__ = "task_label"

    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#6c757d")
    tasks = db.relationship("Task", secondary=task_labels, back_populates="labels")
