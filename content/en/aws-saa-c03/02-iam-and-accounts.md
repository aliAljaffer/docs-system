# 2. IAM and Accounts

**Goal:** Control who can access AWS and what each identity can do.

## Core rule

Apply the [[principle-of-least-privilege|principle of least privilege]]. Grant only the access that a user or resource needs.

## IAM policies

An [[security-iam|IAM]] policy is a JSON document. It states what is allowed or denied, for whom, and on which resources.

| Element | Meaning |
|---|---|
| Version number | Version of the policy language |
| Policy ID | Identifier for the policy |
| Statement | One or more permission blocks, each with an ID |
| Action | Operations that the policy governs |
| Effect | Allow or Deny |
| Principal | The user that the policy applies to |
| Resource | AWS resources that the policy applies to |
| Condition (optional) | Conditions that must be met. If they are not met, the policy is ignored. |

## Passwords and MFA

- A password policy enforces strong passwords.
- [[multi-factor-authentication|Multi-factor authentication]] (MFA) adds a second layer of security. Device types:
  - Virtual, such as Google Authenticator
  - Universal 2nd Factor (U2F) hardware, such as YubiKey
  - SurePassID key fob for AWS GovCloud

## Access methods

| Method | Credentials |
|---|---|
| AWS CLI | Access key and secret key |
| AWS Management Console | Password and MFA |
| AWS SDK | Access key and secret key |

## Roles

An IAM role lets an AWS resource access other AWS services. For example, a [[compute-lambda|Lambda]] function uses a role with [[storage-s3|S3]] permissions to upload a file.

## Reports

| Report | Scope | Shows |
|---|---|---|
| Credentials report | Account | Status and activity of each user |
| Access Advisor | User | Which services the user accesses |

## Conditions

| Condition key | Effect |
|---|---|
| `aws:SourceIp` | Restricts the client IP address that makes API calls |
| `aws:RequestedRegion` | Denies access to specific regions |
| `aws:PrincipalOrgID` | Allows or restricts access by [[management-and-governance-organizations|AWS Organizations]] ID |

## Permission boundaries

A permission boundary sets the maximum permissions for a user or role. Groups do not support permission boundaries. Use boundaries with service control policies (SCPs) in Organizations.

## Multiple accounts

- Organizations groups many AWS accounts.
- Control Tower sets up governance guardrails:
  - Preventive guardrails use SCPs. For example, they restrict regions across all accounts.
  - Detective guardrails use [[management-and-governance-config|AWS Config]]. For example, they find untagged resources.
- IAM Identity Center gives one login for:
  - AWS accounts in Organizations
  - Business cloud apps
  - SAML 2.0 apps
  - EC2 Windows instances
- Identity Center uses a built-in identity store or a third-party provider, such as Active Directory or Okta.
- Permission sets are collections of IAM policies.
- Attribute-based access control sets permissions from user attributes. Change an attribute to change access.

## Exam tips

- Use roles to give AWS resources access to other services.
- An explicit Deny blocks an action, even when another policy allows it.
- A permission boundary sets a maximum. It does not grant access.
- Use Access Advisor to see which services a user accesses.
- Identity Center gives one login across many accounts.
- Control Tower preventive guardrails use SCPs. Detective guardrails use AWS Config.

[Next: Compute](03-compute.md)
