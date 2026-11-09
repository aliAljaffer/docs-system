---
title: ✅ 5. Terraform Associate 003
category: Certifications
description: https://www.youtube.com/watch?v=SPcwo0Gq9T8
tags:
- certification
---

<!-- imported from ObsidianVault/studies/cloud-architecht/✅ 5. Terraform Associate 003.md. Edit the source, then run sync.py. -->

# ✅ 5. Terraform Associate 003

`certification`

https://www.youtube.com/watch?v=SPcwo0Gq9T8

![](/assets/vault/pasted-image-20250729212542.webp)
![](/assets/vault/pasted-image-20250729212609.webp)
## `terraform init`
once a Terraform file is ready, `cd` into its directory and run this command.
![](/assets/vault/pasted-image-20250729212734.webp)
![](/assets/vault/pasted-image-20250729212747.webp)
## `terraform plan`
Displays the planned changes. Kinda like `git status`
![](/assets/vault/pasted-image-20250729213026.webp)
## `terraform apply`
Actually runs the `.tf` file.
## `terraform destroy`
Destroys the entire resources found in the `.tf` file. Alternatively, to delete a resource, just comment it out.
## `terraform get`
![](/assets/vault/pasted-image-20250729212844.webp)
## `terraform graph | dot -Tsvg > graph.svg`
Visualize your execution plan
![](/assets/vault/pasted-image-20250729212901.webp)
## Output block
```
output "public_ip" {
	value = aws_eip.example.public_ip
}
```
## `terraform.tfvars`
A file that contains variables
![](/assets/vault/pasted-image-20250729154307.webp)
## Variable Precedence
Terraform loads variables in the following order, with later sources taking precedence over earlier ones
1. Environment variables
2. The `terraform.tfvars` file, if present.
3. The `terraform.tfvars.json` file, if present.
4. Any `*.auto.tfvars` or `*.auto.tfvars.json` files, processed in lexical order of their filenames.
5. Any `-var` and `-var-file` options on the command line, in the order they are provided. (This includes variables set by a Terraform Cloud workspace.)
## Provisioners
### Local-exec
Executes code on the machine that ran `terraform apply`
You can specify an `interpreter`
### Remote-exec
Executes code on a remote target resource after a resource is provisioned
### File
used to copy files from local to resource
### Connection
Tells a provisioner or resource how to establish a connection
like ssh
### Null resource
placeholder resource
"Triggers"
### Data (`terraform_data`)
Recommended to use instead of 
Similar to  but doesn't require the configuration of a provider
Can be used to search
![](/assets/vault/pasted-image-20250729180853.webp)
## Resource Behaviors & Lifecycles
![](/assets/vault/pasted-image-20250729181435.webp)
![](/assets/vault/pasted-image-20250729181517.webp)
## Resource Drift
![](/assets/vault/pasted-image-20250729213148.webp)
### Replace / Taint
![](/assets/vault/pasted-image-20250729213251.webp)
### Import
![](/assets/vault/pasted-image-20250729213412.webp)
### Refresh
![](/assets/vault/pasted-image-20250729213554.webp)
## Troubleshooting
![](/assets/vault/pasted-image-20250729213618.webp)
## Debugging
`TF_LOG=<TRACE | DEBUG | INFO | WARN | ERROR | JSON>`
`TF_LOG_PATH`
## Backends
Where operations are performed and where tfstate snapshots are stored
![](/assets/vault/pasted-image-20250730094634.webp)
