import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from injector import inject
from kubernetes.client import AppsV1Api, CoreV1Api
from kubernetes.client.models import V1Pod
from kubernetes.client.rest import ApiException
from sqlalchemy.exc import IntegrityError

from kubernetes import client, config
from src.torpedo.errors import TorpedoException
from src.torpedo.models import Role
from src.torpedo.repository import Repository
from src.torpedo.web.jwt_auth_utils import (
    get_username_and_roles_from_token,
    required_role_is_present,
    requires_auth,
)

NAMESPACE = "torpili"

jobs = Blueprint("jobs", __name__, url_prefix="jobs")


@jobs.route("/", methods=["GET"])
@requires_auth
def list_jobs():
    # there should be some way in which we know which jobs are currently ongoing (see the TODO in the master script)
    return jsonify({"status": "ok", "message": "this is not implemented yet"})


@jobs.route("/", methods=["POST"])
@inject
@requires_auth
def submit_job(apps_api: AppsV1Api):
    """Submit a new job for execution on the cluster"""

    if not required_role_is_present(Role.SUBMIT_JOBS):
        raise TorpedoException(f"You are not authorized to submit jobs (no '{Role.SUBMIT_JOBS}' role)", 401)

    num_mappers = request.json["num_mappers"]
    num_reducers = request.json["num_reducers"]
    map_func_file = request.json["map_func_file"]
    reduce_func_file = request.json["reduce_func_file"]
    input_file = request.json["input_file"]

    try:

        job_id = 0  # this should be stored somewhere
        master_name = f"master_{job_id}"

        master_pod_spec = {
            "serviceAccountName": "mr-manager-sa",
            "containers": [
                {
                    "name": master_name,
                    "image": "petemp/distsys-mapred-master:latest",
                    "resources": {"limits": {"memory": "128Mi", "cpu": "500m"}},
                }
            ],
        }

        master_deployment_manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": master_name},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"app": master_name}},
                "template": {"metadata": {"labels": {"app": master_name}}, "spec": master_pod_spec},
            },
        }

        apps_api.create_namespaced_deployment(NAMESPACE, master_deployment_manifest)
    except Exception as e:
        raise TorpedoException(f"error while creating master deployment: {e}", 500)

    return jsonify({"status": "ok", "message": f"job submitted successfully"})
