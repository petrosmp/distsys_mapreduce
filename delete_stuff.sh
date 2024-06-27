#!/bin/bash

kubectl delete job master-0
kubectl delete service splitter-service
kubectl delete service mapper-service
kubectl delete service shuffler-service
kubectl delete service reducer-service
kubectl delete statefulset splitter
kubectl delete statefulset mapper
kubectl delete statefulset shuffler
kubectl delete statefulset reducer
