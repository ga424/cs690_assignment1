# Architecture Documentation

These diagrams document the controlled evaluation harness:

- [Execution flow](execution-flow.md): runtime path from `harness.runner` to generated summaries.
- [C4 context and containers](c4-context.md): system boundary and internal Python components.
- [C4 deployment model](c4-deployment.md): workstation, Python runtime, Docker sandbox, repository files, and provider cloud.

The diagrams are descriptive documentation. The source of truth for behavior remains the Python implementation, especially `harness/runner.py`, `harness/sandbox.py`, `harness/docker_entry.py`, and `harness/verify.py`.
