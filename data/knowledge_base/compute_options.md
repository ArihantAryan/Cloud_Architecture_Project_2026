# Compute Options for Startup Workloads

## Serverless Compute (AWS Lambda, Azure Functions, Google Cloud Functions)
Best suited for startups with unpredictable or spiky traffic, small engineering teams,
and a need to minimize operational overhead. Billing is per-invocation and per-millisecond
of execution, so idle time costs nothing. Ideal for event-driven workloads: API backends
with moderate traffic, image/file processing pipelines, webhooks, and scheduled jobs.
Drawbacks include cold-start latency and execution time limits (typically 15 minutes max),
making it a poor fit for long-running batch jobs or workloads needing persistent in-memory
state.

## Container Orchestration (Kubernetes: EKS, AKS, GKE)
Suited for startups with a platform/DevOps engineer on staff, workloads that need fine-grained
control over scaling and networking, or teams already invested in a microservices
architecture. Offers strong portability across clouds and is cost-efficient at moderate-to-high
sustained traffic, but carries meaningful operational complexity and a learning curve.
Not recommended for very early-stage startups (pre-seed, 1-3 engineers) due to setup and
maintenance overhead.

## Managed Container Services (AWS Fargate, Azure Container Apps, Google Cloud Run)
A middle ground between serverless and full Kubernetes. Startups get container flexibility
(custom runtimes, longer execution times, more memory) without managing the underlying
cluster. Cloud Run and Container Apps in particular support scale-to-zero, keeping costs
low during low-traffic periods while allowing longer execution windows than pure serverless
functions. This is often the sweet spot for early-to-growth-stage startups building web
APIs or backend services.

## Traditional Virtual Machines (EC2, Azure VMs, Compute Engine)
Appropriate when a startup needs full OS-level control, is running legacy software with
specific dependencies, or has steady, predictable, high-utilization workloads where
reserved/committed-use pricing significantly reduces cost versus serverless. Requires more
operational management (patching, scaling policies, load balancer configuration) than
managed alternatives.

## Recommendation Heuristics
- Pre-seed/seed stage, small team, uncertain traffic -> serverless or managed containers.
- Series A+, growing team, sustained moderate-to-high traffic -> managed containers or Kubernetes.
- Compute-heavy ML workloads with GPU needs -> managed ML platforms (SageMaker, Vertex AI,
  Azure ML) or GPU-enabled VM instances, not serverless.
