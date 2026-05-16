from sqlalchemy import Column, Integer, String, Text

from core.database import db
from core.models.mixins import PKMixin, TimestampMixin


class AIInteraction(PKMixin, TimestampMixin, db.Model):
    __tablename__ = "ai_interaction"

    user_id = Column(String(36), db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    feature = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, default="")
    model = Column(String(100), default="gpt-4o")
    tokens_used = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
