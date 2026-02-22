import logging
from fastapi import FastAPI, Request
import uvicorn

# Import the Agent from the Dapr SDK
from dapr_agents import Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("k8s-agent")

app = FastAPI()

# Initialize the Drasi Kubernetes observer agent
k8s_observer_agent = Agent(
    name="DrasiK8sObserver",
    role="Infrastructure Monitor",
    instructions=["Monitor Drasi continuous queries for Kubernetes state changes."]
)

@app.get("/dapr/subscribe")
def subscribe():
    """
    Dapr pub/sub registration endpoint.
    """
    logger.info("Registering pub/sub topic with Dapr sidecar...")
    return [{
        "pubsubname": "drasi-pubsub",
        "topic": "k8s-alerts",
        "route": "/k8s-reaction"
    }]

@app.post("/k8s-reaction")
async def react_to_k8s_event(request: Request):
    """
    Handles incoming events from Drasi via Dapr.
    """
    cloud_event = await request.json()
    
    # Extract the actual payload from the CloudEvent wrapper
    event_data = cloud_event.get("data", cloud_event)

    logger.info("Received Drasi event via Dapr")

    if "deletedResults" in event_data:
        deleted_count = len(event_data['deletedResults'])
        logger.info(f"K8s Resource(s) deleted: {deleted_count} items found.")

    if "addedResults" in event_data:
        added_count = len(event_data['addedResults'])
        logger.info(f"K8s Resource(s) added: {added_count} items found.")

    return {"status": "SUCCESS"}

if __name__ == "__main__":
    logger.info("Starting Dapr reactive agent on port 8081...")
    uvicorn.run(app, host="0.0.0.0", port=8081)
