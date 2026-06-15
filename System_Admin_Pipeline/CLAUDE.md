# System Admin Pipeline Context

## 🧭 Domain Context
This pipeline governs AROS execution environments, Conda environments, AWS EC2 orchestration, and database administration.

## ⚖️ Component Rules
- **Self-Healing Environment Policy**: Strictly enforces the L0→L1→L2 `aros-base` Conda-gated architecture for any system-level scripts.
- **Port Allocation**: Adheres to the dynamic port allocation policy (`BACKEND_PORT` and `FRONTEND_PORT`) to prevent parallel swarm job collisions.

## 🚀 Execution
- **Trigger**: Admin workflows like `/aws-dynamic-ec2-orchestration` run from here.
