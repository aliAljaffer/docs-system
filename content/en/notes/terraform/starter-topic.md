---
title: Starter-topic
category: Terraform
description: 'Terraform note: Starter-topic.'
tags:
- terraform
---


# Starter-topic

`terraform`

```terraform
terraform {

	required_providers {
	
	aws = {
	
		source = "hashicorp/aws"
		
		version = "5.80.0"
		
		}
	
	}

}

provider "aws" {

	region = "eu-north-1"
	
	access_key = "<redacted>"
	
	secret_key = "<redacted>"

}

  

# resource name is in the scope of terrafrom

resource "aws_instance" "web" {

	ami = "ami-075449515af5df0d1"
	
	instance_type = "t2.micro"
	
	tags = {
	
		"name" = "HelloWorld"
	
	}

}
```
