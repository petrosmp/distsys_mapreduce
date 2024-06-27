from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.client.models import V1Pod
import os

NAMESPACE = "torpili"
INPUT_FILE = os.getenv("INPUT_FILE", "/mnt/longhorn/input_file")
NUM_SPLITTERS = 1
NUM_SHUFFLERS = 1
NUM_MAPPERS = int(os.getenv("NUM_MAPPERS", 3))
NUM_REDUCERS = int(os.getenv("NUM_REDUCERS", 5))

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
                "args": [INPUT_FILE, str(NUM_MAPPERS)],
                "volumeMounts": [{"mountPath": "/mnt/longhorn", "name": "longhorn-storage"}],
            }
        ],
        "volumes": [{"name": "longhorn-storage", "persistentVolumeClaim": {"claimName": "longhorn-pvc"}}],
    }

    splitter_statefulset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {"name": "splitter", "namespace": "torpili"},
        "spec": {
            "serviceName": "splitter-service",
            "podManagementPolicy": "Parallel",
            "replicas": NUM_SPLITTERS,
            "selector": {"matchLabels": {"app": "splitter"}},
            "template": {"metadata": {"labels": {"app": "splitter"}}, "spec": splitter_spec_dict},
        },
    }

    splitter_service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": "splitter-service"},
        "spec": {"selector": {"app": "splitter"}, "type": "ClusterIP", "ports": [{"port": 7777, "targetPort": 7777}]},
    }

    mapper_spec_dict = {
        "containers": [
            {
                "name": "mapper",
                "env": [
                    {
                        "name": "POD_NAME",
                        "valueFrom": {
                            "fieldRef": {
                                "fieldPath": "metadata.name"
                            }
                        }
                    }
                ],
                "image": "georgestav/mapper:latest",
                "command": ["python", "mapper.py"],
                "volumeMounts": [{"mountPath": "/mnt/longhorn", "name": "longhorn-storage"}],
            }
        ],
        "volumes": [{"name": "longhorn-storage", "persistentVolumeClaim": {"claimName": "longhorn-pvc"}}],
    }

    mapper_statefulset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {"name": "mapper", "namespace": "torpili"},
        "spec": {
            "serviceName": "mapper-service",
            "podManagementPolicy": "Parallel",
            "replicas": NUM_MAPPERS,
            "selector": {"matchLabels": {"app": "mapper"}},
            "template": {"metadata": {"labels": {"app": "mapper"}}, "spec": mapper_spec_dict},
        },
    }

    mapper_service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": "mapper-service"},
        "spec": {"selector": {"app": "mapper"}, "type": "ClusterIP", "ports": [{"port": 7777, "targetPort": 7777}]}
    }


    shuffler_spec_dict = {
        "containers": [
            {
                "name": "shuffler",
                "image": "georgestav/shuffler:latest",
                "env": [
                    {
                        "name": "NUM_REDUCERS",
                        "value": NUM_REDUCERS
                    }
                ],
                "command": ["python", "shuffler.py"],
                "volumeMounts": [{"mountPath": "/mnt/longhorn", "name": "longhorn-storage"}],
            }
        ],
        "volumes": [{"name": "longhorn-storage", "persistentVolumeClaim": {"claimName": "longhorn-pvc"}}],
    }

    shuffler_statefulset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {"name": "shuffler", "namespace": "torpili"},
        "spec": {
            "serviceName": "shuffler-service",
            "podManagementPolicy": "Parallel",
            "replicas": NUM_SHUFFLERS,
            "selector": {"matchLabels": {"app": "shuffler"}},
            "template": {"metadata": {"labels": {"app": "shuffler"}}, "spec": shuffler_spec_dict},
        },
    }

    shuffler_service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": "shuffler-service"},
        "spec": {"selector": {"app": "shuffler"}, "type": "ClusterIP", "ports": [{"port": 7777, "targetPort": 7777}]}
    }


    reducer_spec_dict = {
        "containers": [
            {
                "name": "reducer",
                "env": [
                    {
                        "name": "POD_NAME",
                        "valueFrom": {
                            "fieldRef": {
                                "fieldPath": "metadata.name"
                            }
                        }
                    }
                ],
                "image": "georgestav/reducer:latest",
                "command": ["python", "reducer.py"],
                "volumeMounts": [{"mountPath": "/mnt/longhorn", "name": "longhorn-storage"}],
            }
        ],
        "volumes": [{"name": "longhorn-storage", "persistentVolumeClaim": {"claimName": "longhorn-pvc"}}],
    }

    reducer_statefulset_manifest = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {"name": "reducer", "namespace": "torpili"},
        "spec": {
            "serviceName": "reducer-service",
            "podManagementPolicy": "Parallel",
            "replicas": NUM_REDUCERS,
            "selector": {"matchLabels": {"app": "reducer"}},
            "template": {"metadata": {"labels": {"app": "reducer"}}, "spec": reducer_spec_dict},
        },
    }

    reducer_service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": "reducer-service"},
        "spec": {"selector": {"app": "reducer"}, "type": "ClusterIP", "ports": [{"port": 7777, "targetPort": 7777}]}
    }


    try:

        # create splitters
        try:
            core_api.delete_namespaced_service(namespace=NAMESPACE, name="splitter-service")
        except:
            pass
        core_api.create_namespaced_service(NAMESPACE, splitter_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, splitter_statefulset_manifest)

        splitters: list[V1Pod] = core_api.list_namespaced_pod(NAMESPACE, label_selector="app=splitter").items

        # loop untill all splitters have completed
        i = 0
        while True:
            while i < len(splitters):
                if splitters[i].status.phase == "Completed":
                    splitters.pop(i)
                    i += 1
                    break
            break

        # TODO: could write to a file here (and after each stage) so that if the master is killed, the execution
        # is picked up where it was left of

        print(f"done splitting")

        # create mappers
        core_api.create_namespaced_service(NAMESPACE, mapper_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, mapper_statefulset_manifest)

        mappers: list[V1Pod] = core_api.list_namespaced_pod(NAMESPACE, label_selector="app=mapper").items

        # loop untill all mappers have completed
        i = 0
        while True:
            while i < len(mappers):
                if mappers[i].status.phase == "Completed":
                    mappers.pop(i)
                    i += 1
                    break
            break
        print(f"done mapping")


        # create shufflers
        core_api.create_namespaced_service(NAMESPACE, shuffler_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, shuffler_statefulset_manifest)

        shufflers: list[V1Pod] = core_api.list_namespaced_pod(NAMESPACE, label_selector="app=shuffler").items

        # loop untill all shufflers have completed
        i = 0
        while True:
            while i < len(shufflers):
                if shufflers[i].status.phase == "Completed":
                    shufflers.pop(i)
                    i += 1
                    break
            break
        print(f"done shuffling")


        # create reducers
        core_api.create_namespaced_service(NAMESPACE, reducer_service_manifest)
        apps_api.create_namespaced_stateful_set(NAMESPACE, reducer_statefulset_manifest)

        reducers: list[V1Pod] = core_api.list_namespaced_pod(NAMESPACE, label_selector="app=reducer").items

        # loop untill all reducers have completed
        i = 0
        while True:
            while i < len(reducers):
                if reducers[i].status.phase == "Completed":
                    reducers.pop(i)
                    i += 1
                    break
            break
        print(f"done reducing")


        print("Split & Map & Shuffle & Reduce completed successfully")

        apps_api.delete_namespaced_stateful_set(namespace=NAMESPACE, name="splitter")
        apps_api.delete_namespaced_stateful_set(namespace=NAMESPACE, name="mapper")
        apps_api.delete_namespaced_stateful_set(namespace=NAMESPACE, name="shuffler")
        apps_api.delete_namespaced_stateful_set(namespace=NAMESPACE, name="reducer")
        core_api.delete_namespaced_service(namespace=NAMESPACE, name="splitter-service")
        core_api.delete_namespaced_service(namespace=NAMESPACE, name="mapper-service")
        core_api.delete_namespaced_service(namespace=NAMESPACE, name="shuffler-service")
        core_api.delete_namespaced_service(namespace=NAMESPACE, name="reducer-service")
        print("deleted services & statefulsets successfully")
    except ApiException as e:
        print(f"Exception when creating pod: {e}")


if __name__ == "__main__":
    create_pods()
