#!/bin/bash

kubectl delete job master-0
kubectl delete service mapper-service
kubectl delete service splitter-service
kubectl delete statefulset mapper
kubectl delete statefulset splitter
