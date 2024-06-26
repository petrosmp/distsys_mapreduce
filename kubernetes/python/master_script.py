from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client.models import V1Pod
import os

NAMESPACE = "torpili"
NUM_SPLITTERS = 1
INPUT_FILE = "/mnt/longhorn/input_file"
NUM_MAPPERS = 3

def create_pods():
    config.load_incluster_config()

    core_api = client.CoreV1Api()
    apps_api = client.AppsV1Api()

    splitter_spec_dict = {
        "containers": [
            {
                "name": "splitter",
                "image": "georgestav/splitter:latest",
                "command": ["python", "splitter.py"],
                "args": [
                    INPUT_FILE,
                    str(NUM_MAPPERS)
                ],
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
        ]
    }

    splitter_statefulset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {
            "name": "splitter",
            "namespace": "torpili"
        },
        "spec": {
            "serviceName": "splitter-service",
            "podManagementPolicy": "Parallel",
            "replicas": NUM_SPLITTERS,
            "selector": {
                "matchLabels": {
                    "app": "splitter"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "splitter"
                    }
                },
                "spec": splitter_spec_dict
            }
        }
    }

    splitter_service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "splitter-service"
        },
        "spec": {
            "selector": {
                "app": "splitter"
            },
            "type": "ClusterIP"
        }
    }



    mapper_spec_dict = {
        "containers": [
            {
                "name": "mapper",
                "image": "georgestav/mapper:latest",
                "command": ["python", "mapper.py"],
                "args": [
                    "/mnt/longhorn/split0.txt"
                ],
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
        ]
    }


    mapper_statefulset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {
            "name": "mapper",
            "namespace": "torpili"
        },
        "spec": {
            "serviceName": "mapper-service",
            "podManagementPolicy": "Parallel",
            "replicas": NUM_MAPPERS,
            "selector": {
                "matchLabels": {
                    "app": "mapper"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "mapper"
                    }
                },
                "spec": mapper_spec_dict
            }
        }
    }

    splitter_service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "mapper-service"
        },
        "spec": {
            "selector": {
                "app": "mapper"
            },
            "type": "ClusterIP"
        }
    }

    try:

        # create splitters
        core_api.create_namespaced_service(NAMESPACE, splitter_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, splitter_statefulset_manifest)

        splitters: list[V1Pod] = core_api.list_namespaced_pod(NAMESPACE, label_selector="app=splitter").items

        split_done = False

        while not split_done:
            for i in splitters:
                if i: break

        # create mappers
        core_api.create_namespaced_service(NAMESPACE, splitter_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, splitter_statefulset_manifest)
        


        print("SplitterStatefulSet created successfully")
    except ApiException as e:
        print(f"Exception when creating pod: {e}")

if __name__ == '__main__':
    create_pods()
