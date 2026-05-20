---
ki_name: system-status
ki_title: AROS System Status Monitoring
ki_description: Provides a comprehensive overview of how to programmatically monitor the real-time status, metrics, and health of the Antigravity Research OS (AROS).
author: AROS-mutation-sweeper
---

# AROS System Status Monitoring KI

This Knowledge Item (KI) outlines the key endpoints and data points available for monitoring the AROS ecosystem.

## Core Status Monitoring

The primary endpoint for a high-level system overview is `/api/status`.

- **Fact 1: Check Active Processes**
  The system's current running state, indicating whether a "dream" or "mutation" cycle is active, can be determined by sending a `GET` request to the `/api/status` endpoint.

- **Fact 2: View Scheduled Tasks**
  The same `/api/status` endpoint provides the timestamp for the next scheduled automated run of core processes.

## Detailed Metrics Retrieval

For a more granular view of system performance, the `/api/metrics` endpoint provides detailed, real-time data.

- **Fact 3: Live Memory Metrics**
  The `/api/metrics` endpoint returns a JSON object containing a detailed breakdown of the AROS memory, including the counts of `world_facts` and `experiences`.

- **Fact 4: Swarm Intelligence Metrics**
  This endpoint also provides key performance indicators for the swarm, such as the number of `active_nodes` and `completed_tasks`.
  
- **Fact 5: GEPA Evolution Metrics**
  The `/api/metrics` endpoint provides metrics on the GEPA evolution process, including `failed_traces` and `mutated_skills`.

## Log Analysis

- **Fact 6: Access System Logs**
  The last 100 lines of the system daemon logs can be retrieved programmatically by sending a `GET` request to `/api/logs`. This is crucial for real-time debugging and health checks.

## Validation

To validate the information in this KI, you can use a tool like `curl` or any HTTP client to make `GET` requests to the described endpoints on a running AROS instance. For example:

```bash
# Check the main system status
curl http://localhost:8000/api/status

# Retrieve detailed system metrics
curl http://localhost:8000/api/metrics
```

The responses should be JSON objects containing the data structures described in this document.
