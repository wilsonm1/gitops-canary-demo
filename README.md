# GitOps Canary Demo

A small service and pipeline built to practice progressive delivery ahead of a
Consensus DevOps Engineer interview. It demonstrates the loop the role is
built around: ship code, scan it, hand off to GitOps, release as a canary,
and roll back automatically on failure - with no one touching the cluster.

## What it does

1. Push to `main` triggers GitHub Actions.
2. Tests and lint run in parallel; pip's dependency cache keeps them fast.
3. The image builds with Docker layer caching, then is scanned with Trivy -
   the build fails on HIGH/CRITICAL vulnerabilities.
4. On success, the image is pushed to GHCR and the pipeline commits the new
   tag into `k8s/rollout.yaml` - the GitOps hand-off.
5. Argo CD detects the Git change and syncs the cluster to match.
6. Argo Rollouts releases the new version as a canary: 20% of traffic, an
   automated health check, 60%, another check, then 100%.
7. If a health check fails, the rollout aborts and reverts to the last good
   version automatically.

## Try it locally

```bash
./scripts/setup.sh                     # kind cluster + Argo CD + Argo Rollouts
kubectl argo rollouts get rollout orders -n orders --watch
```

Ship a bad release to see the rollback:

```bash
kubectl set env rollout/orders FAIL_RATE=1 -n orders
```

## Why this exists

This is a personal project, not production code, built to go deeper on
progressive delivery (canary/blue-green releases) - a gap I identified in my
own experience against this specific role.
