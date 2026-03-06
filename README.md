# 🛡️ Reactive Kubernetes Security Agent (Drasi + Dapr PoC)

An event-driven, automated security agent that monitors a Kubernetes cluster's state in real-time and reacts to vulnerability labels using **Drasi** and **Dapr**.

## 🎯 Project Overview
In traditional Site Reliability Engineering (SRE), monitoring agents often struggle with how to efficiently detect state changes in a massive cluster. This Proof of Concept demonstrates a decoupled, **reactive infrastructure** that shifts the compute burden away from the application and into the data layer.

By utilizing Drasi's continuous queries, this system watches the Kubernetes control plane for specific state changes (e.g., a pod being labeled `risk=critical`) and instantly routes that actionable event to an external Python agent via a Dapr Pub/Sub message broker.

## 💡 The Evolution of Event Detection (Why Drasi?)

When designing distributed monitoring systems, engineers typically face three architectural choices. This project uses the third, most modern approach:

### 1. The Polling Method (The Old Way)
* **How it works:** The agent constantly asks the Kubernetes API, *"Are there any critical pods? How about now? Now?"*
* **The Problem:** It creates massive overhead on the control plane, wastes compute cycles, and introduces latency. You only find out about a breach on the next polling cycle.

### 2. The Streaming Method via Kafka/RabbitMQ (The Raw Firehose)
* **How it works:** The system uses Change Data Capture (CDC) to stream *every single event* to a message broker like Kafka. 
* **The Problem:** The application acting as the consumer gets blasted with a firehose of raw logs. The developer has to write complex, heavy code inside the application to filter out 99% of the noise just to find the 1% of critical security events. 

### 3. Continuous Queries with Drasi (The Solution)
* **How it works:** Drasi sits directly on the data source and maintains a graph-based state of the system. We deploy a Continuous Cypher Query (`MATCH (p:Pod) WHERE p.labels.risk = "critical"`). 
* **The Advantage:** Drasi does the heavy lifting. It evaluates the raw streams at the source and **only** triggers a reaction when the exact query condition is met. The Python agent receives zero noise—when it gets a message, it knows exactly what to do.



## 🏗️ Architecture & Tech Stack

* **Environment:** Local K3d cluster running on WSL2 (Ubuntu).
* **Event Detection (Drasi):**
  * **Source:** Watches Kubernetes (`etcd`) for resource changes.
  * **Continuous Query:** Runs the Cypher query filtering for risk labels.
  * **Reaction:** Forwards the matched graph data to the Dapr integration.
* **Message Broker (Dapr + Redis):**
  * Decouples the control plane from the application logic.
  * Routes Drasi reactions to a local Pub/Sub topic (`drasi-events`).
* **The Agent (Python/FastAPI):**
  * Subscribes to the Dapr topic and processes the security events in real-time.

## ⚙️ How to Run Locally

### 1. Prerequisites
* A running local Kubernetes cluster (e.g., K3d/Minikube)
* `kubectl` and `dapr` CLI installed
* Drasi installed in the cluster (`drasi init`)
* Python 3.x with a virtual environment

### 2. Start the Network Bridges
To allow the local Python agent to communicate with the in-cluster Drasi and Redis services, open the following port-forwards:

```bash
# Terminal 1: Redis Pub/Sub Bridge
kubectl port-forward -n drasi-system svc/drasi-redis 6380:6379

# Terminal 2: Drasi API Bridge
kubectl port-forward -n drasi-system svc/drasi-api 8080:8080

3. Start the Python Agent
In a new terminal, activate your virtual environment and start the Dapr sidecar alongside the FastAPI application:
dapr run --app-id my-python-agent \
         --app-port 8000 \
         --dapr-http-port 3500 \
         --resources-path ./components \
         -- uvicorn agent:app --port 8000


Gemini said
This is a fantastic addition. Contrasting Drasi with traditional Polling and raw Streaming (like Kafka) is the exact high-level system design discussion that will catch the eye of a GSoC mentor. It proves you understand why a tool exists, not just how to use it.

In System Engineering, understanding the evolution of data flow—from Polling ➡️ to Event Streaming ➡️ to Continuous Queries—is crucial.

Here is the finalized README.md with the "Evolution of Event Detection" section added right into the architectural insights.

Instructions:
Open your terminal and type nano README.md.

Delete the old content and paste this ultimate version.

Save (Ctrl+O, Enter, Ctrl+X), then add, commit, and push it!

Markdown
# 🛡️ Reactive Kubernetes Security Agent (Drasi + Dapr PoC)

An event-driven, automated security agent that monitors a Kubernetes cluster's state in real-time and reacts to vulnerability labels using **Drasi** and **Dapr**.

## 🎯 Project Overview
In traditional Site Reliability Engineering (SRE), monitoring agents often struggle with how to efficiently detect state changes in a massive cluster. This Proof of Concept demonstrates a decoupled, **reactive infrastructure** that shifts the compute burden away from the application and into the data layer.

By utilizing Drasi's continuous queries, this system watches the Kubernetes control plane for specific state changes (e.g., a pod being labeled `risk=critical`) and instantly routes that actionable event to an external Python agent via a Dapr Pub/Sub message broker.

## 💡 The Evolution of Event Detection (Why Drasi?)

When designing distributed monitoring systems, engineers typically face three architectural choices. This project uses the third, most modern approach:

### 1. The Polling Method (The Old Way)
* **How it works:** The agent constantly asks the Kubernetes API, *"Are there any critical pods? How about now? Now?"*
* **The Problem:** It creates massive overhead on the control plane, wastes compute cycles, and introduces latency. You only find out about a breach on the next polling cycle.

### 2. The Streaming Method via Kafka/RabbitMQ (The Raw Firehose)
* **How it works:** The system uses Change Data Capture (CDC) to stream *every single event* to a message broker like Kafka. 
* **The Problem:** The application acting as the consumer gets blasted with a firehose of raw logs. The developer has to write complex, heavy code inside the application to filter out 99% of the noise just to find the 1% of critical security events. 

### 3. Continuous Queries with Drasi (The Solution)
* **How it works:** Drasi sits directly on the data source and maintains a graph-based state of the system. We deploy a Continuous Cypher Query (`MATCH (p:Pod) WHERE p.labels.risk = "critical"`). 
* **The Advantage:** Drasi does the heavy lifting. It evaluates the raw streams at the source and **only** triggers a reaction when the exact query condition is met. The Python agent receives zero noise—when it gets a message, it knows exactly what to do.



## 🏗️ Architecture & Tech Stack

* **Environment:** Local K3d cluster running on WSL2 (Ubuntu).
* **Event Detection (Drasi):**
  * **Source:** Watches Kubernetes (`etcd`) for resource changes.
  * **Continuous Query:** Runs the Cypher query filtering for risk labels.
  * **Reaction:** Forwards the matched graph data to the Dapr integration.
* **Message Broker (Dapr + Redis):**
  * Decouples the control plane from the application logic.
  * Routes Drasi reactions to a local Pub/Sub topic (`drasi-events`).
* **The Agent (Python/FastAPI):**
  * Subscribes to the Dapr topic and processes the security events in real-time.

## ⚙️ How to Run Locally

### 1. Prerequisites
* A running local Kubernetes cluster (e.g., K3d/Minikube)
* `kubectl` and `dapr` CLI installed
* Drasi installed in the cluster (`drasi init`)
* Python 3.x with a virtual environment

### 2. Start the Network Bridges
To allow the local Python agent to communicate with the in-cluster Drasi and Redis services, open the following port-forwards:

```bash
# Terminal 1: Redis Pub/Sub Bridge
kubectl port-forward -n drasi-system svc/drasi-redis 6380:6379

# Terminal 2: Drasi API Bridge
kubectl port-forward -n drasi-system svc/drasi-api 8080:8080
3. Start the Python Agent
In a new terminal, activate your virtual environment and start the Dapr sidecar alongside the FastAPI application:

Bash
dapr run --app-id my-python-agent \
         --app-port 8000 \
         --dapr-http-port 3500 \
         --resources-path ./components \
         -- uvicorn agent:app --port 8000
4. Trigger the Automation (The Watch)
Create a "malicious" pod in the cluster to simulate a security vulnerability.

kubectl run threat-simulation-pod --image=nginx --labels="risk=critical"

Result: The moment the Kubernetes API registers the pod, Drasi detects the label, fires the reaction through Dapr, and the Python agent wakes up instantly to log the event data.

🚀 Future Roadmap
Auto-Remediation: Implement logic inside the Python agent to automatically issue a kubectl delete command upon receiving a critical pod event, creating a fully self-healing cluster mechanic.
