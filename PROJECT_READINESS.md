# GSoC 2026: Reactive Agents with Drasi & Dapr — System Readiness

## Project Deliverables Checklist

| Deliverable | Status | Notes |
|-------------|--------|-------|
| **1. Drasi Router Reaction (Python)** | 🟡 Partial | See below |
| **2. Dapr Agents SDK Extensions** | 🔴 Not Started | |
| **3. Ambient Agent Demo** | 🔴 Not Started | |

---

## 1. Drasi Router Reaction (Python)

**Required:**
- Configurable microservice that routes Drasi events to Dapr Pub/Sub as **CloudEvents**
- **Dynamic routing rules** (topic selection based on event content)
- **Embedded MCP Server** for agents to discover queries at runtime

**Current state:**

| Component | Status | What you have |
|-----------|--------|---------------|
| HTTP endpoint receiving Drasi events | ✅ | `router.py` — `/receive` POST handler |
| CloudEvents format | 🔴 | Raw JSON only; need `type`, `source`, `specversion`, `data` |
| Dapr Pub/Sub publish | 🔴 | No `DaprClient.publish_event()` calls |
| Dynamic routing rules | 🔴 | No rule engine (topic = f(event)) |
| MCP Server | 🔴 | Not implemented |
| Drasi → Router plumbing | 🟡 | HTTP Reaction exists; Query container was offline |

**Next steps:**
- Add CloudEvents envelope to outgoing payloads
- Integrate `DaprClient.publish_event(pubsub_name, topic_name, data)`
- Implement routing rules (e.g., config file or API)
- Add MCP server (e.g., `mcp` Python package)

---

## 2. Dapr Agents SDK Extensions

**Required:**
- Python module: `dapr_agents.extensions.drasi`
- Pydantic models for Drasi events
- `@drasi_trigger` decorator (CloudEvent validation + subscription)

**Current state:**

| Component | Status |
|-----------|--------|
| dapr-agents installed | 🔴 | `pip install dapr-agents` not run |
| dapr_agents.extensions.drasi | 🔴 | Module does not exist |
| Pydantic models | 🟡 | Pydantic in venv; no Drasi-specific models |
| @drasi_trigger decorator | 🔴 | Not implemented |

**Next steps:**
```bash
pip install dapr-agents
# Create: dapr_agents/extensions/drasi/__init__.py
# Define: DrasiEvent, DrasiAddedEvent, etc. (Pydantic)
# Implement: @drasi_trigger decorator wrapping Dapr pub/sub subscription
```

---

## 3. Ambient Agent Demo

**Required:**
- End-to-end reference architecture
- Detects critical DB changes
- Triggers Dapr Agent workflow

**Current state:**
- Drasi Kubernetes source (pods) works
- No DB source (PostgreSQL, etc.) wired for “critical” events
- No Dapr Agent workflow defined

---

## Infrastructure Readiness

| Component | Status | Notes |
|-----------|--------|-------|
| Drasi installed | ✅ | k8s-events source available |
| Dapr in cluster | ✅ | dapr-system namespace |
| Drasi PostDaprPubSub | ✅ | In drasi-resources.yaml |
| Query container | 🟡 | Was offline; may need restart |
| Dapr CLI (local) | ✅ | v1.16.9 |
| Dapr Python SDK | ✅ | dapr in venv |
| Python 3.12 | ✅ | In use |

---

## Immediate Actions (Priority Order)

### 1. Fix Drasi pipeline
```bash
# Wait for query container, then:
drasi list querycontainer -n drasi-system   # Verify default is available
drasi apply -f pod-watch-query.yaml -n drasi-system
# Fix debug-reaction.yaml: queries format (map not list - see error)
```

### 2. Fix debug reaction YAML
Use `queries: { pod-watch: {} }` (map format). Updated in debug-reaction.yaml.

### 3. Install Dapr Agents
```bash
pip install dapr-agents
```

### 4. Use PostDaprPubSub for reference
Drasi’s built-in `PostDaprPubSub` Reaction already publishes to Dapr Pub/Sub. Study its config and payload format before building your Smart Router.

### 5. Transform router.py into Smart Router
- Accept Drasi HTTP Reaction payloads
- Wrap in CloudEvents
- Publish to Dapr Pub/Sub with `DaprClient`
- Add routing rules and MCP server

---

## Summary

**Overall readiness: ~25%**

Foundation is in place (Drasi, Dapr, basic router). Still needed:

1. Drasi CQ + Reactions working (query container + YAML fixes)
2. `router.py` → Smart Router (CloudEvents, Dapr Pub/Sub, rules, MCP)
3. `dapr_agents.extensions.drasi` module
4. Ambient Agent demo

Recommended first milestone: **end-to-end Drasi → HTTP → your router → Dapr Pub/Sub → simple subscriber** before adding MCP and Dapr Agents.
