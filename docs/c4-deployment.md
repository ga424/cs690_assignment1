# C4 Deployment Model

This deployment view describes where the controlled evaluation runs and where each dependency lives. The local workstation is the execution host; provider APIs are reached over the network, while candidate code runs in a separate Docker container with networking disabled.

```mermaid
C4Deployment
    title CS690 controlled evaluation deployment model

    Deployment_Node(workstation, "Student workstation", "macOS, Linux, or Windows", "Runs the Python virtual environment and Docker Desktop or Docker Engine") {
        Deployment_Node(pythonRuntime, "Python runtime", "Python 3.11-3.14", "Runs the harness modules") {
            Container(runner, "Experiment runner", "harness.runner", "Orchestrates generation, grading, metrics, and reports")
            Container(verification, "Verification command", "harness.verify", "Checks the frozen dataset and sandbox without an API key")
        }
        Deployment_Node(dockerHost, "Docker Engine", "Docker", "Builds and starts the sandbox image") {
            Deployment_Node(sandboxContainer, "Candidate sandbox container", "python:3.11.15-slim-bookworm", "One short-lived container per candidate") {
                Container(candidateExecutor, "Candidate executor", "harness/docker_entry.py", "Executes candidate source and tests; emits one JSON verdict")
            }
        }
        Deployment_Node(repository, "Repository files", "Local filesystem", "Configuration, tasks, prompts, candidates, results, and summaries") {
            ContainerDb(inputs, "Frozen inputs", "conditions.json and tasks/cs690_eval20.json", "Fixed controls and task dataset")
            ContainerDb(outputs, "Run artifacts", "results/, prompts/, and candidates/", "Manifest, raw rows, summaries, and saved answers")
        }
    }

    Deployment_Node(providerCloud, "Model provider cloud", "HTTPS API", "External service selected by conditions.json") {
        Container(providerApi, "Provider API", "OpenAI or Anthropic", "Generates candidate answers")
    }

    Rel(runner, inputs, "Reads")
    Rel(verification, inputs, "Reads")
    Rel(runner, providerApi, "Sends prompts over HTTPS")
    Rel(runner, outputs, "Writes")
    Rel(verification, outputs, "Writes verification record")
    Rel(runner, dockerHost, "Starts containers")
    Rel(dockerHost, candidateExecutor, "Runs with --network none, read-only root, caps dropped, CPU/memory/PID limits")
    Rel(candidateExecutor, runner, "Returns JSON verdict through standard output")
```
