# 🚀 Drasi K8s Watcher (GSoC 2026)

Hey! I'm an undergrad CS student, and this is my proof-of-concept project for my Google Summer of Code (GSoC) 2026 proposal with **Drasi**. 

## 🤔 What does this do?
It connects Drasi to a live Kubernetes cluster, listens for system events (like a Pod crashing or being created), and routes that data to a custom Python script using Dapr. Basically, it's a real-time event observer for K8s.

## 🛠️ Tech Stack
* **Core:** Drasi, Dapr
* **Platform:** Kubernetes (k3d) running on WSL2 (Ubuntu 24.04)
* **Logic:** Python 3.12

## 💻 How to run it locally

**1. Set up the environment:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

**2. Deploy the Drasi components:**
\`\`\`bash
# Fix the K8s context secret so Drasi can authenticate
./fix-k8s-context-secret.sh

# Apply the source and continuous query
kubectl apply -f k8s-source.yaml
kubectl apply -f pod-watch-query.yaml
\`\`\`

## 🐛 The Grind (Bugs I Squashed)
Building this wasn't just copy-pasting YAML. Here are a few distributed system headaches I had to solve:
* **Rust Panics:** Debugged a `CurrentContextNotSet` panic in the Drasi Reactivator pod by figuring out exactly how the `kubeConfig` secret needs to be injected.
* **WSL2 Resource Limits:** Realized my Drasi sources were ghosting me because Dapr placement services were silently failing due to RAM pressure in my WSL setup.
* **Namespace Headaches:** Fixed routing disconnects by ensuring all Drasi components and secrets were strictly isolated in the `drasi-system` namespace.
