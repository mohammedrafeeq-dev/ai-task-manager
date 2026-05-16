from sqlalchemy import Column, String

from core.database import db
from core.models.mixins import PKMixin, TimestampMixin


class Organization(PKMixin, TimestampMixin, db.Model):
    __tablename__ = "organization"

    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"<Organization {self.slug}>"
