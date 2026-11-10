---
title: Assignment
category: DevOps
description: 'DevOps note: Assignment.'
tags:
- devops
---


# Assignment

`devops`

## Errors
- What you did
	- I used `terraform init`
- What you expected to happen
	- The modules would download and `.terraform` folder would appear
- What you tried
	- Nothing
- Screenshot/Error code
```bash
[ali ~/my-clone/ecommerce-app-three-tier-azure-db-ih]$ tf init
Terraform initialized in an empty directory!

The directory has no Terraform configuration files. You may begin working
with Terraform immediately by creating Terraform configuration files.
```
## Resources
- ~~RG~~
- ~~Vnet~~
- ~~2 Subnets~~
- ~~2 NSG~~
- ~~App Service (FE + BE)~~
- ~~Azure SQL Database~~
## Workflow | CI/CD | GitHub Actions
### Two Jobs
1. Build And Push FE + BE to Dockerhub
2. Provision infrastructure using Terraform
### Three Jobs
~~1. Build And Push FE to Dockerhub
	1. Checkout the repository
	2. Login to Dockerhub (Probably using docker action)
	3. Build the frontend using frontend Dockerfile (Probably using docker action)
	4. Push to dockerhub using `latest` and `commit` tags (Probably using docker action)
~2. Build And Push BE to Dockerhub
	5. Checkout the repository
	6. Login to Dockerhub (Probably using docker action)
	7. Build the backend using backend Dockerfile (Probably using docker action)
	8. Push to dockerhub using `latest` and `commit` tags (Probably using docker action)
~3. Provision infrastructure using Terraform
	9. Checkout the repository
	10. I need an action that sets up Terraform
	11. I need to pass variable values to Terraform (GitHub Actions secrets!) `TF_VAR_`
	12. Login to Azure
	13. (Optionally) Terraform Plan
	14. CD to Terraform folder
	15. `terraform init`
	16. Terraform Apply (with Auto Approve!)
