#!/usr/bin/env bash
# Local demo cluster: kind + Argo CD + Argo Rollouts. Needs Docker Desktop running.
set -euo pipefail

kind create cluster --name canary-demo

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

kubectl -n argocd rollout status deploy/argocd-server --timeout=300s
kubectl apply -f argocd/application.yaml

echo "Watch the rollout:  kubectl argo rollouts get rollout orders -n orders --watch"
