from flask_login import UserMixin
from sqlalchemy import Column, Enum, String
from werkzeug.security import check_password_hash, generate_password_hash

from core.database import db
from core.models.mixins import OrganizationMixin, PKMixin, TimestampMixin


class User(UserMixin, PKMixin, TimestampMixin, db.Model):
    __tablename__ = "user"

    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    organization_id = Column(
        String(36), db.ForeignKey("organization.id", ondelete="SET NULL"), nullable=True
    )
    role = Column(Enum("admin", "member", name="user_role"), default="member", nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
