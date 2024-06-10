from sqlalchemy.orm import Mapped, mapped_column

from src.torpedo.models import Base


class Token(Base):
    """
    Tokens are used to authenticate users and enforce authorization.

    The process is as follows:
        - when a user logs in, they get a JWT token which contains their
          username and their permissions. This token is also saved to the
          database (that's what this model is for).
        - when a user tries to access a protected resource (i.e. an endpoint)
          we first check if the token exists in the databse and then if the
          permission needed to access this endpoint is present in the token's
          claims.
        - when a user logs out, the token is deleted from the database.
          ^ this is the only reason why tokens are stored in the database.
            Everything else could be achieved by just using JWT tokens, but we
            need a way to force invalidate a token so we can provide user logout
            functionality.
    """

    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token_str: Mapped[str] = mapped_column(unique=True)

    def __init__(self, token_str: str):
        self.token_str = token_str

    def __repr__(self) -> str:
        return f"Token(id={self.id}, token_str={self.token_str})"
