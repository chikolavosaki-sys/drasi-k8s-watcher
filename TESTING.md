# Drasi + Dapr Smart Router – Testing Guide (GSoC 2026)

End-to-end testing for your Drasi Kubernetes source → Continuous Query → Reaction pipeline with Python router.

---

## Prerequisites

- ✅ Drasi source `k8s-events` is available (`drasi list source -n drasi-system`)
- ✅ Kubernetes cluster (k3d-drasi-dev) running

---

## Phase 1: Test Dapr Client (`test_connection.py`)

Dapr client needs a Dapr sidecar. Two options:

### Option A: Local with Dapr CLI

```bash
# Install Dapr CLI if needed: https://docs.dapr.io/getting-started/install-dapr-cli/
dapr run --app-id test-app -- python test_connection.py
```

### Option B: Inside a Dapr-injected pod

Deploy your app to Kubernetes with Dapr sidecar injection; the client will connect to the local sidecar.

---

## Phase 2: Verify Drasi Pipeline (Debug Reaction)

### Step 1: Apply the Continuous Query

```bash
drasi apply -f pod-watch-query.yaml -n drasi-system
drasi list query -n drasi-system
```

### Step 2: Apply the Debug Reaction (logs events)

```bash
drasi apply -f debug-reaction.yaml -n drasi-system
drasi list reaction -n drasi-system
```

### Step 3: Access Debug UI (optional)

```bash
kubectl port-forward -n drasi-system svc/pod-watch-debug-gateway 8080:8080
# Open http://localhost:8080 in browser
```

### Step 4: Trigger events

Create/delete a Pod to generate events:

```bash
kubectl run test-pod --image=nginx --restart=Never
# Check Debug UI or: kubectl logs -n drasi-system -l app=pod-watch-debug -f
kubectl delete pod test-pod
```

---

## Phase 3: Test Your Router (`router.py`)

### Step 1: Start router locally

```bash
cd ~
python -m uvicorn router:app --host 0.0.0.0 --port 6000
```

### Step 2: Check reachability from cluster

From k3d, pods reach the host at `host.k3d.internal`. Ensure nothing blocks port 6000.

### Step 3: Apply HTTP Reaction

```bash
drasi apply -f http-reaction-router.yaml -n drasi-system
```

### Step 4: Trigger events and watch router logs

```bash
# In another terminal, create a pod
kubectl run event-test --image=busybox --restart=Never -- sleep 30
# You should see "Event received: {...}" in the router terminal
kubectl delete pod event-test
```

---

## Phase 4: Deploy Router to Kubernetes (optional)

For production-like testing, deploy the router as a Service:

```bash
# Build and push your image, or use a simple deployment
kubectl create deployment smart-router --image=python:3.12 --port=6000 -n default
kubectl expose deployment smart-router --port=6000 -n default
# Update http-reaction-router.yaml baseUrl to: http://smart-router.default.svc.cluster.local:6000
drasi apply -f http-reaction-router.yaml -n drasi-system
```

---

## Useful Commands

| Command | Purpose |
|---------|---------|
| `drasi list source -n drasi-system` | Check source status |
| `drasi list query -n drasi-system` | List Continuous Queries |
| `drasi list reaction -n drasi-system` | List Reactions |
| `drasi describe reaction pod-watch-http -n drasi-system` | Reaction details |
| `kubectl get pods -n drasi-system` | Drasi pods |

---

## Troubleshooting

- **Source not available**: Run `./fix-k8s-context-secret.sh drasi-system` and re-apply the source
- **Reaction not receiving events**: Ensure CQ subscribes to the correct source id (`k8s-events`)
- **HTTP Reaction 404/connection refused**: Confirm router is running and reachable from the cluster (`host.k3d.internal` from k3d)
