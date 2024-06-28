## A custom MapReduce implementation on a Kubernetes-managed cluster.

This repository was created as the semester project of the INF-419 Principles of Distributed Software Systems course at the Technical University of Crete in June 2024.

Read on for more information regarding repository structure, a presentation, a demonstration of the project in action & more.

  <figure>
      <img src="./cluster_architecture.svg" alt="Container on Image"   />
      <!-- <figcaption>An elephant at sunset</figcaption> -->
  </figure>

### Presentation & Demo
`<links here>`

### Repository Structure
- <a href="./flask-manager-service/"> **`/flask-manager-service/`**</a> contains the implementation of the manager service, which is responsible for handling all user interaction and authentication and creating the master job
- <a href="./kubernetes/">**`/kubernetes/`**</a> contains the cluster configuration. More specifically:
  - <a href="./kubernetes/auth/">**`/kubernetes/auth/`**</a> contains the manifests for the auth DB and the Flask API implementing the manager service
  - <a href="./kubernetes/longhorn/">**`/kubernetes/longhorn/`**</a> contains the longhorn persistent volume and claims manifests
  - <a href="./kubernetes/master-node-python/">**`/kubernetes/master-node-python/`**</a> contains the code that the master job executes, as well as everything needed to build a docker image from it
  - <a href="./kubernetes/rbac/">**`/kubernetes/rbac/`**</a> contains the manifests for the `ServiceAccount` that gives the manager and master nodes the rights to manage jobs in the cluster
- <a href="./node_frontend/">**`/node_frontend/`**</a> contains the files for the frontend web application - user interface
- <a href="./torpedo_algorithm/">**`/torpedo_algorithm/`**</a> contains the files that implement the map, reduce, shuffle and split jobs

### Dependencies:
| **package / tool** | **purpose** |
|:---:|:---:|
| Kubernetes | Cluster Orchestration & Fault Tolerance |
| Longhorn | Kubernetes Persistent Storage |
| Headlamp | Kubernetes Cluster Monitoring |
| Docker | Containerization |
| Flask | API Development |
| PyJWT | Token-Based Authentication |
| SQLAlchemy| ORM |
| psycopg | DB Connection |
| Alembic | DB Migrations |
| PostgreSQL | Database Management |
| HTML, JS, CSS | Web UI |
| nodeJS | Web UI |


### MapReduce Paper
The MapReduce paper can be found <a href="https://www.usenix.org/legacy/publications/library/proceedings/osdi04/tech/full_papers/dean/dean.pdf">here</a>.
