---
title: aws database
category: AWS
description: Databases store semi-structured and structured data. This is the primary
  difference between storage and database.
tags:
- aws
- services
---


# aws database

`aws` `services`

Databases store semi-structured and structured data. This is the primary difference between [[aws-storage|storage]] and database.

## Types
- Relational - Rows and columns
- Non-Relational
Databases are what makes querying and accessing data easier.

## DB Services

| Service | Type | Notes |
|---|---|---|
| **Relational Database Service (RDS)** | Relational | Support for most common SQL-based databases such as MySQL, MariaDB, Oracle, etc |
| **Amazon Aurora** | Relational | Fully managed RDBS service for MySQL and PostgresSQL. Highly available, durable, scalable, and secure. Can be [[serverless]] |
| **DynamoDB** | Non-Relational | Primarily NoSQL database from AWS, designed to be extremely fast, available, and scalable. Can scale to billions of records with guaranteed consistent data retrieval |
| **DocumentDB** | Non-Relational | NoSQL document database for MongoDB |
## Other services
- [[analytics-redshift|redshift]]
- **Elasticache**
- **[[migration-database-migration-service|Database Migration Service]] (DMS)**
	- On-premise database to AWS
	- **SQL -> NoSQL**
