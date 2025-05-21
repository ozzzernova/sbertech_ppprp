#!/bin/bash

curl -L https://istio.io/downloadIstio | sh -
cd istio-* && export PATH=$PWD/bin:$PATH && cd ../

istioctl install --set profile=default -y
kubectl label namespace default istio-injection=enabled

kubectl apply -f kuber/deploy.yaml
kubectl apply -f kuber/gateway.yaml
kubectl apply -f kuber/virtual_service.yaml
kubectl apply -f kuber/destination.yaml

kubectl wait --for=condition=ready pod -l app=hw-app --timeout=60s