---
title: IAM
category: AWS
description: Roles = "virtual" users (NOT human-controlled) that need to use AWS services
tags:
- aws
- services
---


# IAM

`aws` `services`


### IAM Policies Inheritance
- Inline Policy: Sole policy dedicated to a group-less user

| Element | Required | Meaning |
|---|---|---|
| Version | - | Version number |
| Id | Optional | - |
| Statement | Required | One or more statements |
| SID | Optional | Statement ID |
| Effect | - | Allow or deny |
| Principal | - | Account/user/role the policy is applied to |
| Action | - | List of actions this policy allows or denies |
| Resource | - | List of resources to which the action is applied to |
| Condition | Optional | Conditions for when this policy is in effect. One or more conditions to satisfy for the policy to be applicable, otherwise the policy is ignored |

IAM-Policy
### IAM Password Policy
- Strong Password = higher security
- Password Policy can be set to have min length, alphanumeric, lowercase, etc.
- Can expire passwords every X days and prevent password re-use
### Multi-Factor Authentication (MFA)
**RECOMMENDED!!**
- You want to protect your Root Accounts and IAM users
- **MFA** = password *you know* + security device *you own*
#### MFA device options

| Device type | Examples | Note |
|---|---|---|
| Virtual MFA Device | Google Authenticator, Authy | Phone only |
| Universal 2nd Factor Security Key (U2F) | YubiKey | - |
| Hardware Key Fob MFA Device | Gemalto | - |
| Hardware Key Fob MFA Device **for AWS GovCloud** | SurePassID | - |
### Access to AWS
- AWS Management Console (password + MFA)
- AWS CLI (access keys)
- AWS SDK (access keys)
Access Keys are NOT to be shared.
### IAM Roles
Some AWS services will need to perform actions on your behalf, to do so, we assign permissions to AWS services with IAM Roles.

Roles = "virtual" users (NOT human-controlled) that need to use AWS services
### IAM Credentials Report (Account-level)
- Report that lists all your account's users and statuses
### IAM Access Advisor (User-level)
- Access Advisor shows the service permissions granted to a user and when those services were last accessed.
- Used to revise policies
### IAM Guidelines & Best Practices
- Don't use the root account except for AWS account setup
- One physical user = one AWS user
- Assign users to groups and assign permissions to groups
- Create a string password policy
- Use and enforce MFA
- Create and use ROLES
- Use access keys for CLI / SDK
- Audit permissions of your account using IAM Credentials Report & IAM Access Advisor
### Summary
- As best practice, employ [[principle-of-least-privilege|principle of least privilege]].
-  are JSON documents detailing what can and can't be done, by who and on what service. A policy contains: Version Number, Policy ID, Statement(s). See the policy elements table above.
-  can be set to adhere to cybersecurity rules to enforce strong passwords by users.
- An addition layer of security can be added by enforcing [[multi-factor-authentication|multi factor authentication]] devices. These devices come in different formats:
	- Virtual (Google Authenticator)
	- Universal 2nd Factory (Physical, U2F): YubiKey
	- SurePassID's Key Fob for AWS GovCloud.
-  provide a way for AWS resources to have access to other AWS resources. 
	- Examples include [[compute-lambda|Lambda]] needing a [[storage-s3|S3]] Role to be able to upload a file programmatically.
- Access to AWS can be done in three ways:
	- AWS CLI - access keys and secret keys
	- AWS Management Console - password + MFA
	- AWS SDK - access keys and secret keys
- Reports can be acquired account-level using Credentials Report, showing status of each user in the account and activity. And user-level with Access Advisor, to see which services the accounts are using.
- 
