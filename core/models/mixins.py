import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import declared_attr
from core.database import db


class PKMixin:
    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )


class TimestampMixin:
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class OrganizationMixin:
    @declared_attr
    def organization_id(self):
        return Column(
            String(36),
            ForeignKey("organization.id", ondelete="CASCADE"),
            nullable=False,
        )
