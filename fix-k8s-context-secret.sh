#!/bin/bash
# Recreate k8s-context secret with current-context preserved.
# Fixes: CurrentContextNotSet panic in Drasi Kubernetes source proxy/reactivator.

set -e

NAMESPACE="${1:-drasi-system}"

echo "=== Fixing k8s-context secret (current-context must be set) ==="
echo "Target namespace: $NAMESPACE"
echo ""

# --minify keeps only current context and ensures current-context field is included
# (required by kube client libraries; missing causes CurrentContextNotSet panic)
echo "[1/3] Extracting kubeconfig with current-context..."
kubectl config view --raw --minify -o yaml > /tmp/kubeconfig-fix.yaml

# Verify current-context exists
if ! grep -q "current-context:" /tmp/kubeconfig-fix.yaml; then
    echo "ERROR: current-context is missing from kubeconfig. Check your kubectl config."
    exit 1
fi
echo "  ✓ current-context found"

# Replace server address for in-cluster access
# Handles: 127.0.0.1, 0.0.0.0, host.docker.internal, etc.
echo "[2/3] Rewriting server for in-cluster (kubernetes.default.svc:443)..."
sed -E 's|(server:\s+https://)([^:/]+)(:[0-9]+)?|\1kubernetes.default.svc:443|g' /tmp/kubeconfig-fix.yaml > /tmp/kubeconfig-fix-final.yaml

# Recreate secret
echo "[3/3] Recreating k8s-context secret..."
kubectl delete secret k8s-context -n "$NAMESPACE" --ignore-not-found
kubectl create secret generic k8s-context --from-file=context=/tmp/kubeconfig-fix-final.yaml -n "$NAMESPACE"

# Cleanup
rm -f /tmp/kubeconfig-fix.yaml /tmp/kubeconfig-fix-final.yaml

echo ""
echo "Done. Restart the source proxy/reactivator to pick up the new secret:"
echo "  drasi delete source k8s-events -n $NAMESPACE"
echo "  drasi apply -f k8s-source-drasi-format.yaml -n $NAMESPACE"
