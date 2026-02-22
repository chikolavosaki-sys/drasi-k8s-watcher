import logging
import asyncio
from dapr_agents import DurableAgent
from dapr_agents.workflow.runners import AgentRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("k8s-agent")

async def main():
    logger.info("Initializing Drasi K8s Observer Agent...")
    
    # Define the DurableAgent (Workflow-backed for reliability)
    k8s_observer_agent = DurableAgent(
        name="DrasiK8sObserver",
        role="Infrastructure Monitor",
        instructions=[
            "You monitor Drasi continuous queries for Kubernetes state changes.",
            "Analyze incoming event payloads to track infrastructure health."
        ]
    )

    # Initialize the official Agent Runner
    runner = AgentRunner()

    logger.info("Subscribing reactive agent to Drasi pub/sub...")
    
    # Subscribe the agent directly to the Dapr pub/sub topic
    await runner.subscribe(
        agent=k8s_observer_agent,
        pubsub_name="drasi-pubsub",
        topic="k8s-alerts",
        port=8081
    )

if __name__ == "__main__":
    asyncio.run(main())
