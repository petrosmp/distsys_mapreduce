import logging
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any

import jwt
from flask import Blueprint, current_app, jsonify, request
from injector import inject

from src.torpedo.errors import AuthException, TorpedoException
from src.torpedo.models import User
from src.torpedo.repository import Repository
from src.torpedo.web.jwt_auth_utils import get_token_from_auth_header, requires_auth

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
@inject
def login(repository: Repository) -> Any:
    """Login a user with the given username & password."""
    username = request.json["username"]
    password = request.json["password"]

    user = repository.authenticate_user(username, password)

    if not user:
        raise AuthException("wrong credentials", HTTPStatus.CONFLICT)

    token = create_and_save_token(user, repository)

    if not token:
        raise TorpedoException("unexpected DB error", HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"status": "ok", "token": token})


@auth.route("/logout", methods=["POST"])
@requires_auth
@inject
def logout(repository: Repository):
    """Log the currently logged in user out (i.e. invalidate their token)."""
    token = get_token_from_auth_header()

    try:
        repository.delete_token_by_str(token)
    except Exception as e:
        logging.error(f"Error while deleting token.\n{e}")
        logging.exception(e)
        raise TorpedoException("unexpected DB error", HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"status": "ok"})


def create_and_save_token(user: User, repository: Repository):
    token = jwt.encode(
        {
            "username": user.username,
            "roles": user.roles,
            "exp": datetime.now() + timedelta(hours=1),  # token is valid for 1 hour
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    try:
        repository.save_token(token)
        return token
    except Exception as e:
        logging.error(f"Error while saving token.\n{e}")
        logging.exception(e)
        return None
