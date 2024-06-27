from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.client.models import V1Pod
import os
import job_state


NAMESPACE = "torpili"
INPUT_FILE = os.getenv("INPUT_FILE", "/mnt/longhorn/input_file")
NUM_SPLITTERS = 1
NUM_SHUFFLERS = 1
NUM_MAPPERS = int(os.getenv("NUM_MAPPERS", 3))
NUM_REDUCERS = int(os.getenv("NUM_REDUCERS", 5))
JOB_ID = os.getenv("JOB_ID")
STATE_FILE_NAME = "STATE"
JOB_TTL_AFTER_COMPLETION_SECONDS = 60

def save_state(state):
    with open(f"{job_dir}/{STATE_FILE_NAME}", 'w') as file:
        file.write(str(state))


splitter_job_manifest = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": f"splitter-{JOB_ID}",
        "namespace": "torpili"
    },
    "spec": {
        "completions": NUM_SPLITTERS,
        "completionMode": "Indexed",
        "parallelism": NUM_SPLITTERS,
        "ttlSecondsAfterFinished": JOB_TTL_AFTER_COMPLETION_SECONDS,
        "template": {
            "metadata": {
                "labels": {
                    "app": f"splitter-{JOB_ID}"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": f"splitter-{JOB_ID}",
                        "image": "georgestav/splitter:latest",
                        "env": [
                            {
                                "name": "JOB_ID",
                                "value": JOB_ID
                            }
                        ],
                        "command": ["python", "splitter.py"],
                        "args": [INPUT_FILE, str(NUM_MAPPERS)],
                        "volumeMounts": [
                            {
                                "mountPath": "/mnt/longhorn",
                                "name": "longhorn-storage"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "longhorn-storage",
                        "persistentVolumeClaim": {
                            "claimName": "longhorn-pvc"
                        }
                    }
                ],
                "restartPolicy": "OnFailure"
            }
        }
    }
}

mapper_job_manifest = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": f"mapper-{JOB_ID}",
        "namespace": "torpili"
    },
    "spec": {
        "completions": NUM_MAPPERS,
        "completionMode": "Indexed",
        "parallelism": NUM_MAPPERS,
        "ttlSecondsAfterFinished": JOB_TTL_AFTER_COMPLETION_SECONDS,
        "template": {
            "metadata": {
                "labels": {
                    "app": f"mapper-{JOB_ID}"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": f"mapper-{JOB_ID}",
                        "image": "georgestav/mapper:latest",
                        "env": [
                            {
                                "name": "POD_NAME",
                                "valueFrom": {
                                    "fieldRef": {
                                        "fieldPath": "metadata.name"
                                    }
                                }
                            },
                            {
                                "name": "JOB_ID",
                                "value": JOB_ID
                            }
                        ],
                        "command": ["python", "mapper.py"],
                        "volumeMounts": [
                            {
                                "mountPath": "/mnt/longhorn",
                                "name": "longhorn-storage"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "longhorn-storage",
                        "persistentVolumeClaim": {
                            "claimName": "longhorn-pvc"
                        }
                    }
                ],
                "restartPolicy": "OnFailure"
            }
        }
    }
}

shuffler_job_manifest = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": f"shuffler-{JOB_ID}",
        "namespace": "torpili"
    },
    "spec": {
        "completions": NUM_SHUFFLERS,
        "completionMode": "Indexed",
        "parallelism": NUM_SHUFFLERS,
        "ttlSecondsAfterFinished": JOB_TTL_AFTER_COMPLETION_SECONDS,
        "template": {
            "metadata": {
                "labels": {
                    "app": f"shuffler-{JOB_ID}"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": f"shuffler-{JOB_ID}",
                        "image": "georgestav/shuffler:latest",
                        "env": [
                            {
                                "name": "NUM_REDUCERS",
                                "value": str(NUM_REDUCERS)
                            },
                            {
                                "name": "JOB_ID",
                                "value": JOB_ID
                            }
                        ],
                        "command": ["python", "shuffler.py"],
                        "volumeMounts": [
                            {
                                "mountPath": "/mnt/longhorn",
                                "name": "longhorn-storage"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "longhorn-storage",
                        "persistentVolumeClaim": {
                            "claimName": "longhorn-pvc"
                        }
                    }
                ],
                "restartPolicy": "OnFailure"
            }
        }
    }
}

reducer_job_manifest = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": f"reducer-{JOB_ID}",
        "namespace": "torpili"
    },
    "spec": {
        "completions": NUM_REDUCERS,
        "completionMode": "Indexed",
        "parallelism": NUM_REDUCERS,
        "ttlSecondsAfterFinished": JOB_TTL_AFTER_COMPLETION_SECONDS,
        "template": {
            "metadata": {
                "labels": {
                    "app": f"reducer-{JOB_ID}"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": f"reducer-{JOB_ID}",
                        "image": "georgestav/reducer:latest",
                        "env": [
                            {
                                "name": "POD_NAME",
                                "valueFrom": {
                                    "fieldRef": {
                                        "fieldPath": "metadata.name"
                                    }
                                }
                            },
                            {
                                "name": "JOB_ID",
                                "value": JOB_ID
                            }
                        ],
                        "command": ["python", "reducer.py"],
                        "volumeMounts": [
                            {
                                "mountPath": "/mnt/longhorn",
                                "name": "longhorn-storage"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "longhorn-storage",
                        "persistentVolumeClaim": {
                            "claimName": "longhorn-pvc"
                        }
                    }
                ],
                "restartPolicy": "OnFailure"
            }
        }
    }
}


def create_pods(state: int):
    config.load_incluster_config()

    batch_api = client.BatchV1Api()

    def wait_for_job_completion(job_name, namespace):
        w = watch.Watch()
        for event in w.stream(batch_api.list_namespaced_job, namespace=namespace):
            job = event['object']
            if job.metadata.name == job_name:
                if job.status.succeeded == job.spec.completions:
                    w.stop()


    try:

        if state < job_state.SPLIT_PHASE_ONGOING:
            batch_api.create_namespaced_job(NAMESPACE, splitter_job_manifest)

            state = job_state.SPLIT_PHASE_ONGOING
            save_state(state)

        if state < job_state.SPLIT_PHASE_DONE:
            wait_for_job_completion(f"splitter-{JOB_ID}", NAMESPACE)

            state = job_state.SPLIT_PHASE_DONE
            save_state(state)

        if state < job_state.MAP_PHASE_ONGOING:
            batch_api.create_namespaced_job(NAMESPACE, mapper_job_manifest)
            
            state = job_state.MAP_PHASE_ONGOING
            save_state(state)

        if state < job_state.MAP_PHASE_DONE:
            wait_for_job_completion(f"mapper-{JOB_ID}", NAMESPACE)

            state = job_state.MAP_PHASE_DONE
            save_state(state)

        if state < job_state.SHUFFLE_PHASE_ONGOING:
            batch_api.create_namespaced_job(NAMESPACE, shuffler_job_manifest)
           
            state = job_state.SHUFFLE_PHASE_ONGOING
            save_state(state)

        if state < job_state.SHUFFLE_PHASE_DONE:
            wait_for_job_completion(f"shuffler-{JOB_ID}", NAMESPACE)

            state = job_state.SHUFFLE_PHASE_DONE
            save_state(state)

        if state < job_state.REDUCE_PHASE_ONGOING:
            batch_api.create_namespaced_job(NAMESPACE, reducer_job_manifest)

            state = job_state.REDUCE_PHASE_ONGOING
            save_state(state)


        if state < job_state.REDUCE_PHASE_DONE:
            wait_for_job_completion(f"reducer-{JOB_ID}", NAMESPACE)

            state = job_state.REDUCE_PHASE_DONE
            save_state(state)

        # we only reach here if everything that had to be run was run
        state = job_state.FINISHED
        save_state(state)
        print("deleted services & statefulsets successfully")
    except ApiException as e:
        print(f"Exception when creating pod: {e}")
        exit(1)

if __name__ == "__main__":

    job_dir = f"/mnt/longhorn/job_{JOB_ID}"

    if os.path.exists(job_dir):
        try:
            with open(f"{job_dir}/{STATE_FILE_NAME}", 'r') as file:
                content = file.read()
            if content:
                state = int(content)
            else:
                state = job_state.INITIALIZED
        except FileNotFoundError:   # catch cases where crash happened before even saving state file
            state = job_state.INITIALIZED
    else:
        os.makedirs(job_dir)
        os.makedirs(f"{job_dir}/mapper_out")
        os.makedirs(f"{job_dir}/reducer_out")
        os.makedirs(f"{job_dir}/shuffler_out")
        os.makedirs(f"{job_dir}/split_out")
        with open(f"{job_dir}/{STATE_FILE_NAME}", 'w') as file:
            file.write(str(job_state.INITIALIZED))
        state = job_state.INITIALIZED

    create_pods(state)
