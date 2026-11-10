---
title: Aws database
category: AWS
description: Databases store semi-structured and structured data. This is the primary
  difference between storage and database.
tags:
- aws
- services
---


# Aws database

`aws` `services`

Databases store semi-structured and structured data. This is the primary difference between [[aws-storage|storage]] and database.

## Types
- Relational - Rows and columns
- Non-Relational
Databases are what makes querying and accessing data easier.

## Relational DB Services
1. **Relational Database Service (RDS)**
	1. Support for most common SQL-based databases such as MySQL, MariaDB, Oracle, etc
2. **Amazon Aurora**
	1. Fully managed RDBS service for MySQL and PostgresSQL
	2. Highly available, durable, scalable, and secure.
	3. Can be [[serverless]] 
## Non-Relational DB Services
1. **DynamoDB**
	1. Primarily NoSQL database from AWS, designed to be extremely fast, available, and scalable
	2. Can scale to billions of records with guaranteed consistent data retrieval.
2. **DocumentDB**
	1. NoSQL document database for MongoDB.
## Other services
- [[analytics-redshift|redshift]]
- **Elasticache**
- **[[migration-database-migration-service|Database Migration Service]] (DMS)**
	- On-premise database to AWS
	- **SQL -> NoSQL**
