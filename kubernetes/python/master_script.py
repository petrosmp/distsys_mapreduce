from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os

NAMESPACE = "torpili"
NUM_SPLITTERS = 1


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
                    "worerw\n efwf w\n 23r ef\n",
                    "3"
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


    try:
        core_api.create_namespaced_service(NAMESPACE, splitter_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, splitter_statefulset_manifest)

        print("SplitterStatefulSet created successfully")
    except ApiException as e:
        print(f"Exception when creating pod: {e}")

if __name__ == '__main__':
    create_pods()
