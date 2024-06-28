from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import sessionmaker

from src.torpedo.errors import NoSuchUserException
from src.torpedo.models import Role, Token, User


class Repository:
    """Manages interactions with persistent storage."""

    def __init__(self, Session: sessionmaker[_Session]):  # noqa: N803
        self.Session: sessionmaker[_Session] = Session  # noqa: N803

    def authenticate_user(self, username: str, password: str) -> int | None:
        with self.Session() as session:
            session.expire_on_commit = (
                False  # allows us to use the user outside of the session (detached) to create the token
            )
            user: User | None = (
                session.query(User)
                .where(
                    User.username == username,
                )
                .first()
            )

            if user and user.check_password(password):
                return user

            return None

    def create_user(self, username: str, password: str, roles: set[Role]) -> User:
        user = User(username, password, roles)
        with self.Session.begin() as session:
            session.expire_on_commit = (
                False  # allows us to use objects detached from the session. not a good idea in general
            )
            session.add(user)
        return user

    def user_add_roles(self, username: str, roles: set[Role]):
        """
        Add the given role(s) to an existing user.

        Has no effect if user already has the given role(s).

        Raises `NoSuchUserException` if no user exists with the given username
        """
        with self.Session.begin() as session:
            query_result = (
                session.query(User)
                .filter_by(
                    username=username,
                )
                .first()
            )
            if query_result is not None:
                query_result.roles |= roles
                session.flush()
            else:
                raise NoSuchUserException(f"No user found with username '{username}'")

    def user_remove_roles(self, username: str, roles: set[Role]):
        """
        Remove the given role(s) from an existing user.

        Has no effect if user does not have the given role(s).

        Raises `NoSuchUserException` if no user exists with the given username.
        """
        with self.Session.begin() as session:
            query_result = (
                session.query(User)
                .filter_by(
                    username=username,
                )
                .first()
            )
            if query_result is not None:
                query_result.roles -= roles
                session.flush()
            else:
                raise NoSuchUserException(f"No user found with username '{username}'")

    def save_token(self, token_str: str):
        """Given a JWT token as a string, create a database entry for it."""
        token = Token(token_str)
        with self.Session.begin() as session:
            session.add(token)
            session.flush()
        return token

    def delete_token_by_str(self, token_str: str):
        """
        Delete the token with the given str.

        Has no effect, raises no error if no such token exists.
        """
        with self.Session.begin() as session:
            token: Token | None = (
                session.query(Token)
                .where(
                    Token.token_str == token_str,
                )
                .first()
            )
            if token:
                session.delete(token)
                session.flush()

    def delete_token_by_id(self, token_id: int):
        """
        Deletes the token with the given ID.

        Has no effect, raises no error no such token exists.

        This is preferred to deleting by str because since the ID is a primary key, there is an index
        on it (see https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS)
        and thus the operation should be faster.
        """
        with self.Session.begin() as session:
            token: Token | None = (
                session.query(Token)
                .where(
                    Token.id == token_id,
                )
                .first()
            )

            if token:
                session.delete(token)
                session.flush()

    def token_is_valid(self, token_str: str):
        """Returns true if the given token string exists in the database, false otherwise."""
        with self.Session() as session:
            token: Token | None = (
                session.query(Token)
                .where(
                    Token.token_str == token_str,
                )
                .first()
            )

            return token is not None

    def token_is_valid_by_id(self, token_id: str):
        """Returns true if the given token ID exists in the database, false otherwise."""
        with self.Session() as session:
            token: Token | None = (
                session.query(Token)
                .where(
                    Token.id == token_id,
                )
                .first()
            )

            return token is not None
