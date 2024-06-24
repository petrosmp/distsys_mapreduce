from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from typing import Any, ParamSpec  # noqa: TYP001

import flask_injector
import jwt
from flask import current_app, request
from injector import inject

from src.torpedo.errors import AuthException, TorpedoException
from src.torpedo.repository import Repository


def get_token_from_auth_header() -> str:
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthException("Authorization header is expected", HTTPStatus.UNAUTHORIZED)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthException("Authorization header must start with Bearer", HTTPStatus.UNAUTHORIZED)
    elif len(parts) == 1:
        raise AuthException("Token not found", HTTPStatus.UNAUTHORIZED)
    elif len(parts) > 2:
        raise AuthException("Authorization header must be Bearer token", HTTPStatus.UNAUTHORIZED)

    token = parts[1]
    return token


P = ParamSpec("P")  # allows us to do this https://typing.readthedocs.io/en/latest/spec/generics.html#id4


@inject
def requires_auth(f: Callable[P, Any]) -> Callable[P, Any]:
    """Determines if the Access Token is valid"""

    @wraps(f)
    @inject
    def decorated(repository: Repository, *args: P.args, **kwargs: P.kwargs) -> Any:
        token = get_token_from_auth_header()
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthException("token is expired", HTTPStatus.UNAUTHORIZED)
        except Exception:
            raise AuthException("Unable to parse authentication token.", HTTPStatus.UNAUTHORIZED)

        # also check that the token is in the DB (and thus the user hasn't logged out, invalidating the token)
        try:
            valid = repository.token_is_valid(token)
        except Exception:
            raise TorpedoException("unexpected DB error", HTTPStatus.INTERNAL_SERVER_ERROR)

        if not valid:
            raise AuthException("token has been invalidated", HTTPStatus.UNAUTHORIZED)

        from src.torpedo.web.module import TorpedoModule

        return flask_injector.Injector(modules=[TorpedoModule]).call_with_injection(f, *args, **kwargs)

    return decorated


def required_role_is_present(required_role: str) -> bool:
    """Determines if the required role is present in the Access Token
    Args:
        required_scope (str): The role required to access the resource
    """
    token = get_token_from_auth_header()
    unverified_claims = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
    if unverified_claims.get("roles"):
        token_roles = set(unverified_claims["roles"])
        if required_role in token_roles:
            return True
    return False


def get_username_and_roles_from_token():
    """
    Return the username and the roles that the logged in user has from the token
    that is present in the Authorization header.
    """
    username = None
    roles = {}

    token = get_token_from_auth_header()
    unverified_claims: dict[str, str] = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
    if unverified_claims.get("roles"):
        roles = set(unverified_claims["roles"])
    if unverified_claims.get("username"):
        username = unverified_claims["username"]

    return username, roles
