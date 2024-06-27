from http import HTTPStatus

from flask import Blueprint, jsonify, request
from injector import inject
from kubernetes.client import AppsV1Api, BatchV1Api

from src.torpedo.errors import TorpedoException
from src.torpedo.models import Role
from src.torpedo.web.jwt_auth_utils import required_role_is_present, requires_auth

NAMESPACE = "torpili"

jobs = Blueprint("jobs", __name__)


@jobs.route("/jobs", methods=["GET"])
@requires_auth
def list_jobs():
    # there should be some way in which we know which jobs are currently ongoing (see the TODO in the master script)
    return jsonify({"status": "ok", "message": "this is not implemented yet"})


@jobs.route("/submit_job", methods=["POST"])
@requires_auth
@inject
def submit_job(apps_api: AppsV1Api):
    """Submit a new job for execution on the cluster"""

    if not required_role_is_present(Role.SUBMIT_JOBS.value):
        raise TorpedoException(
            f"You are not authorized to submit jobs (no '{Role.SUBMIT_JOBS.value}' role)", HTTPStatus.UNAUTHORIZED
        )

    num_mappers = request.json["num_mappers"]
    num_reducers = request.json["num_reducers"]
    map_func_file = request.json["map_func_file"]
    reduce_func_file = request.json["reduce_func_file"]
    input_file = request.json["input_file"]

    try:

        job_id = 0  # this should be stored somewhere
        master_name = f"master-{job_id}"

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
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"name": master_name},
            "spec": {
                "completions": 1,
                "template": {
                    "metadata": {"labels": {"app": master_name}},
                    "spec": {
                        "restartPolicy": "Never",
                        "serviceAccountName": "mr-manager-sa",
                        "containers": [
                            {
                                "name": master_name,
                                "image": "petemp/distsys-mapred-master:latest",
                                "resources": {"limits": {"memory": "128Mi", "cpu": "500m"}},
                                "env": [
                                    {"name": "NUM_MAPPERS", "value": str(num_mappers)},
                                    {"name": "NUM_REDUCERS", "value": str(num_reducers)},
                                    {"name": "INPUT_FILE", "value": str(input_file)},
                                ]
                            }
                        ],
                    }
                },
                "backoffLimit": 4  # Optional: Number of retries before marking the Job as failed
            }
        }

        batch_api = BatchV1Api()
        batch_api.create_namespaced_job(NAMESPACE, master_deployment_manifest)
    except Exception as e:
        raise TorpedoException(f"error while creating master deployment: {e}", HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"status": "ok", "message": f"job submitted successfully"})
