from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

# This is the routing  wrap into a custom SDK decorator!
@dapr_app.subscribe(pubsub='drasi-pubsub', topic='drasi-events')
def wake_up_agent(event: dict):
    print("--------------------------------------------------", flush=True)
    print(" AWAKE! Drasi detected a change in the K8s cluster!", flush=True)
    print(f"Event Data: {event}", flush=True)
    print("--------------------------------------------------", flush=True)
    return {"status": "SUCCESS"}
