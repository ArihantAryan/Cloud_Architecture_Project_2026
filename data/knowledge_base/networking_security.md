# Networking and Security for Startup Cloud Architectures

## API Gateway and Load Balancing
Startups exposing an API should place a managed API gateway (Amazon API Gateway, Azure API
Management, Google Cloud API Gateway/Apigee) in front of backend services to handle
authentication, rate limiting, request validation, and routing. For services running on
containers or VMs, a managed load balancer (ALB, Azure Load Balancer, Cloud Load Balancing)
should distribute traffic across instances and enable zero-downtime deployments.

## Content Delivery Network (CDN)
Any startup serving static assets, images, or frontend applications to a geographically
distributed user base should use a CDN (CloudFront, Azure CDN, Cloud CDN) to reduce latency
and offload traffic from origin servers. This is low-cost and should be adopted early
regardless of company stage.

## Identity and Access Management
Startups should adopt the principle of least privilege from day one: use IAM roles/policies
scoped to specific services rather than broad admin credentials, and avoid embedding
long-lived credentials in application code. Managed identity services (IAM, Azure AD/Entra
ID, Cloud IAM) should be used for both human access and service-to-service authentication.

## Compliance Considerations
Startups handling payment data must design around PCI-DSS requirements, typically by
offloading card handling to a payment processor (Stripe, Braintree) rather than storing
card data directly. Startups handling health data (HIPAA) or EU personal data (GDPR) need
to select regions and services with appropriate compliance certifications and enable
encryption at rest and in transit as a baseline, not an afterthought.

## Secrets Management
Application secrets (API keys, database credentials) should be stored in a managed secrets
service (AWS Secrets Manager, Azure Key Vault, Google Secret Manager) rather than
environment files or source control, even for early-stage MVPs, since retrofitting secrets
management after a security incident is far costlier than adopting it upfront.

## Recommendation Heuristics
- Any public-facing API -> API gateway + managed load balancer.
- Any static or media content -> CDN, regardless of startup stage.
- Regulated data (payments, health, EU personal data) -> compliance-certified services and
  encryption at rest/in transit are mandatory baseline requirements, not optional add-ons.
