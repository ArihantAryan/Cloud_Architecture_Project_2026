# Cost Optimization Strategies for Startup Cloud Spend

## Right-Sizing and Autoscaling
Startups frequently over-provision compute resources out of caution. Autoscaling policies
(scale-out on load, scale-to-zero when idle) should be configured from the start for any
compute service that supports it, rather than provisioning fixed capacity for peak load.

## Committed Use Discounts
Once a startup has at least 6-12 months of stable usage data for a given workload, reserved
instances, savings plans, or committed use discounts (available on all three major clouds)
can reduce compute costs by 30-60% compared to on-demand pricing. This should not be adopted
before usage patterns are well understood, since committing early to the wrong instance
type or region locks in inefficiency.

## Storage Lifecycle Policies
Object storage costs can be significantly reduced by configuring lifecycle policies that
automatically transition infrequently accessed data to cheaper storage tiers (e.g., S3
Infrequent Access, S3 Glacier, Azure Cool/Archive, Cloud Storage Nearline/Coldline) and by
deleting or archiving logs and temporary data past a defined retention window.

## Free Tier and Startup Credit Programs
All three major cloud providers offer startup credit programs (AWS Activate, Microsoft for
Startups, Google Cloud for Startups) providing $1,000-$100,000+ in credits depending on
funding stage and program tier. New startups should apply for these before committing
significant budget to infrastructure.

## Multi-Cloud Cost Consideration
Startups should generally avoid spreading workloads across multiple cloud providers early
on purely for cost reasons; the operational overhead of managing multiple providers usually
outweighs marginal cost savings until the company reaches meaningful scale with dedicated
platform engineering resources.

## Recommendation Heuristics
- Early stage, uncertain usage -> pay-as-you-go/on-demand pricing, apply for startup credits.
- Stable usage for 6+ months -> evaluate committed use discounts for predictable workloads.
- Any object storage usage -> configure lifecycle policies from the start.
- Avoid multi-cloud architectures before Series B/C scale unless there is a specific
  redundancy or data-residency requirement driving it.
