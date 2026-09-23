# Database and Storage Options for Startups

## Managed Relational Databases (Amazon RDS/Aurora, Azure SQL/PostgreSQL, Cloud SQL)
The default choice for startups with structured, relational data and a need for strong
consistency (e.g., transactional systems, user accounts, billing). Aurora and Cloud SQL
offer serverless/auto-scaling tiers that are cost-effective for startups with variable
load, avoiding the need to provision for peak capacity upfront. Recommended as the default
for most SaaS startups unless there is a specific reason to choose otherwise.

## NoSQL / Document Databases (DynamoDB, Cosmos DB, Firestore)
Well suited for startups building applications with flexible or evolving schemas, very high
read/write throughput needs, or global low-latency access patterns (e.g., real-time apps,
gaming leaderboards, IoT data ingestion). DynamoDB and Firestore both offer generous
pay-per-use free tiers, making them attractive for early-stage products validating product-
market fit before committing to fixed infrastructure costs.

## In-Memory Caching (Redis via ElastiCache, Azure Cache for Redis, Memorystore)
Recommended as an add-on (not a primary datastore) once an application has measurable
read-heavy traffic on frequently-accessed data, or needs session storage / rate limiting.
Not typically needed at the earliest MVP stage unless the product is latency-sensitive by
nature (e.g., real-time bidding, chat applications).

## Object Storage (S3, Azure Blob Storage, Cloud Storage)
The standard choice for storing unstructured data: user uploads, static assets, backups,
and data lake staging. Extremely low cost at rest, and all three major providers offer
tiered storage classes (hot/cool/archive) that startups should use to reduce costs on
infrequently accessed data.

## Data Warehousing (Redshift, BigQuery, Synapse Analytics)
Not recommended for early-stage startups without a dedicated analytics need. Becomes
relevant once a startup has meaningful data volume and requires complex analytical queries
across large datasets that a transactional database cannot serve efficiently.

## Recommendation Heuristics
- Structured/transactional data, unclear scale -> managed relational DB with autoscaling tier.
- High-throughput, flexible schema, or global distribution -> NoSQL document database.
- Any user-facing file/media storage -> object storage, tiered by access frequency.
- Defer data warehousing and heavy caching layers until there is a demonstrated need.
