from typing import Any

from flask import jsonify

from src.torpedo.errors import TorpedoException


def handle_generic_exception(ex: TorpedoException) -> Any:
    response = jsonify({"status": "error", "message": ex.error})
    response.status_code = ex.status_code
    return response
