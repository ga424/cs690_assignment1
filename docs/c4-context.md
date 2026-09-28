# C4 Context And Containers

The system boundary is the controlled evaluation harness. The model providers and Docker engine are external systems that the harness integrates with.

## System context

```mermaid
C4Context
    title CS690 controlled evaluation system context

    Person(student, "Student or researcher", "Runs the experiment and reviews the resulting summaries")
    System(harness, "Controlled evaluation harness", "Generates model solutions, grades them in a sandbox, and computes pass@k metrics")
    System_Ext(providerApis, "Model provider APIs", "OpenAI or Anthropic API used to generate candidate answers")
    System_Ext(dockerEngine, "Docker Engine", "Builds and runs the isolated candidate sandbox")
    System_Ext(fileSystem, "Local repository filesystem", "Stores configuration, frozen tasks, prompts, candidates, raw results, and summaries")

    Rel(student, harness, "Runs and inspects")
    Rel(harness, providerApis, "Sends fixed prompts and receives candidates")
    Rel(harness, dockerEngine, "Builds images and runs one container per candidate")
    Rel(harness, fileSystem, "Reads inputs and writes run artifacts")
```

## Container view

```mermaid
C4Container
    title Controlled evaluation harness containers

    Person(student, "Student or researcher", "Runs the command-line tools")
    System_Ext(providerApis, "Model provider APIs", "OpenAI or Anthropic")
    System_Ext(dockerEngine, "Docker Engine", "Runs isolated candidate containers")

    System_Boundary(harness, "Controlled evaluation harness") {
        Container(runner, "Experiment runner", "Python", "Loads controls, requests candidates, coordinates grading, scoring, and reporting")
        Container(provider, "Provider adapters", "Python", "Sends prompts and records model responses and usage metadata")
        Container(grader, "Grader and task loader", "Python", "Extracts Python and pairs each candidate with the frozen tests")
        Container(sandbox, "Sandbox launcher", "Python", "Starts a constrained Docker container and reads its JSON verdict")
        Container(metrics, "Metrics and report writer", "Python", "Computes pass@1, pass@2, confidence intervals, and summaries")
        ContainerDb(files, "Repository artifacts", "JSON, JSONL, TXT, and Python files", "Conditions, frozen tasks, prompts, candidates, raw results, and summaries")
    }

    Container_Ext(candidate, "Candidate sandbox", "Python in Docker", "Executes model-written code and tests with no network and restricted resources")

    Rel(student, runner, "Runs")
    Rel(runner, files, "Reads controls and tasks; writes artifacts")
    Rel(runner, provider, "Requests one generation per attempt")
    Rel(provider, providerApis, "Calls provider API")
    Rel(runner, grader, "Submits generated answer")
    Rel(grader, sandbox, "Submits extracted source and tests")
    Rel(sandbox, dockerEngine, "Builds or starts image")
    Rel(sandbox, candidate, "Runs source and tests")
    Rel(candidate, sandbox, "Returns one JSON verdict")
    Rel(runner, metrics, "Passes graded rows")
    Rel(metrics, files, "Writes summaries")
```
