import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from injector import inject
from sqlalchemy.exc import IntegrityError

from src.torpedo.errors import TorpedoException
from src.torpedo.repository import Repository
from src.torpedo.web.jwt_auth_utils import (
    get_username_and_roles_from_token,
    requires_auth,
)

home = Blueprint("home", __name__)


@home.route("/", methods=["GET"])
@requires_auth
def home_page():
    username, roles = get_username_and_roles_from_token()
    return jsonify({"status": "ok", "message": f"you are successfully logged in as {username} with roles {roles}"})


@home.route("/register", methods=["POST"])
@inject
def create_user(repository: Repository):
    """Create a new user with the given username, password and roles."""
    username = request.json["username"]
    password = request.json["password"]
    roles = set(request.json["roles"])

    try:
        user = repository.create_user(username, password, roles)
    except IntegrityError:  # actually a psycopg.errors.UniqueViolation, reraised from sqlalchemy
        raise TorpedoException("user with such data already exists", HTTPStatus.CONFLICT)
    except Exception as e:
        logging.error(f"Error while creating user.\n{e}")
        logging.exception(e)
        raise TorpedoException("unexpected DB error", HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"status": "ok", "message": f"user {user.username} successfully created (user ID: {user.id})"})
