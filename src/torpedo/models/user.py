import enum

from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from src.torpedo.models import Base


class Role(str, enum.Enum):
    """Determines ability to perform tasks around the system"""

    ADMIN = "admin"
    READ_STORAGE = "read_storage"
    WRITE_STORAGE = "write_storage"
    SUBMIT_JOBS = "submit_jobs"
    TRACK_JOBS = "track_jobs"
    MANAGE_USERS = "manage_users"


class User(Base):
    """Holds data for a user"""

    __tablename__ = "users"  # avoid name colision with postgres 'user' table

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    roles: Mapped[set[Role]] = mapped_column(ARRAY(String), nullable=True)

    def __init__(self, username: str, password: str, roles: set[Role]):
        self.username = username
        self._set_password(password)
        self.roles = roles

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"

    def is_admin(self) -> bool:
        return Role.ADMIN in self.roles

    def has_role(self, role: Role):
        return role in self.roles

    def _set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
