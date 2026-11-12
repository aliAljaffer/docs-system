---
title: Security Token Service
category: AWS
description: AWS Security Token Service (STS) is a web service that enables you to
  request temporary, limited-privilege credentials for AWS Identity and Access Management
  (IAM) users or federated users. These temp
tags:
- aws
- services
---


# Security Token Service

`aws` `services`

AWS Security Token Service (STS) is a web service that enables you to request temporary, limited-privilege credentials for AWS Identity and Access Management (IAM) users or federated users. These temporary credentials work almost identically to long-term access key credentials, but with the advantage of being temporary and automatically expiring.
## Core Concepts
**Temporary Security Credentials** consist of:
- Access Key ID
- Secret Access Key
- Session Token
- Expiration timestamp
These credentials are typically valid for 15 minutes to 12 hours, depending on the service used and configuration.
## STS Operations
### AssumeRole
Allows an IAM user or service to assume a role and receive temporary credentials.
#### AWS CLI example
```bash
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/MyRole \
    --role-session-name MySession
```
#### Response
```json
{
    "Credentials": {
        "AccessKeyId": "ASIACKCEVSQ6C2EXAMPLE",
        "SecretAccessKey": "9drTJvcXLB89EXAMPLELB8923FB892xMFI",
        "SessionToken": "AQoEXAMPLEH4aoAH0gNCAPyJxz4BlCFFxWNE1OPTgk5TthT...",
        "Expiration": "2023-11-15T23:28:33Z"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": "AROA3XFRBF535PLBIFPI4:MySession",
        "Arn": "arn:aws:sts::123456789012:assumed-role/MyRole/MySession"
    }
}
```
#### Use cases
- Cross-account access
- Service-to-service authentication
- Temporary elevation of privileges
- CI/CD pipeline authentication
### AssumeRoleWithWebIdentity
Enables federated users from web identity providers (Google, Facebook, Amazon, or any OpenID Connect provider) to assume a role.
#### AWS CLI example
```bash
aws sts assume-role-with-web-identity \
    --role-arn arn:aws:iam::123456789012:role/WebIdentityRole \
    --role-session-name WebIdentitySession \
    --web-identity-token eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```
#### Use cases
- Mobile applications using social login
- Web applications with federated identity
- Single sign-on (SSO) implementations
- Third-party application integration
### AssumeRoleWithSAML
Allows users authenticated via SAML 2.0 to assume a role and receive temporary credentials.

#### AWS CLI example
```bash
aws sts assume-role-with-saml \
    --role-arn arn:aws:iam::123456789012:role/SAMLRole \
    --principal-arn arn:aws:iam::123456789012:saml-provider/MySAMLProvider \
    --saml-assertion base64-encoded-saml-assertion
```
#### Use cases
- Active Directory integration
- Corporate SSO solutions
- SAML-based identity federation
- Enterprise authentication systems
### GetSessionToken
Provides temporary credentials for existing IAM users, typically used for MFA scenarios.
#### AWS CLI example
```bash
aws sts get-session-token \
    --duration-seconds 3600 \
    --serial-number arn:aws:iam::123456789012:mfa/user \
    --token-code 123456
```
#### Use cases
- Multi-factor authentication scenarios
- Temporary credential refresh
- Enhanced security for sensitive operations
- Long-term credential protection
### GetCallerIdentity
Returns information about the IAM user or role whose credentials are used to call the operation.
#### AWS CLI example
```bash
aws sts get-caller-identity
```
#### Response
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/DevUser"
}
```
#### Use cases
- Identity verification
- Debugging authentication issues
- Account validation
- Audit trail creation
### GetFederationToken
Returns temporary credentials for federated users without requiring them to have IAM identities.

#### AWS CLI example
```bash
aws sts get-federation-token \
    --name FederatedUser \
    --duration-seconds 3600 \
    --policy '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:GetObject","Resource":"arn:aws:s3:::mybucket/*"}]}'
```
#### Use cases
- Temporary access for external users
- Limited-scope credential distribution
- Application-specific permissions
- Proxy authentication scenarios
## Common Usage Patterns
### Using Temporary Credentials
After obtaining temporary credentials, you can use them in several ways:
#### Environment variables

```bash
export AWS_ACCESS_KEY_ID=ASIACKCEVSQ6C2EXAMPLE
export AWS_SECRET_ACCESS_KEY=9drTJvcXLB89EXAMPLELB8923FB892xMFI
export AWS_SESSION_TOKEN=AQoEXAMPLEH4aoAH0gNCAPyJxz4BlCFFxWNE1OPTgk5TthT...
```
#### AWS CLI profile
```bash
aws configure set aws_access_key_id ASIACKCEVSQ6C2EXAMPLE --profile temp
aws configure set aws_secret_access_key 9drTJvcXLB89EXAMPLELB8923FB892xMFI --profile temp
aws configure set aws_session_token AQoEXAMPLEH4aoAH0gNCAPyJxz4BlCFFxWNE1OPTgk5TthT... --profile temp
```
### Cross-Account Access Scenario
#### Step 1: Create trust policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111122223333:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
#### Step 2: Assume role
```bash
aws sts assume-role \
    --role-arn arn:aws:iam::444455556666:role/CrossAccountRole \
    --role-session-name CrossAccountSession
```
#### Step 3: Use temporary credentials
```bash
aws s3 ls --profile temp-cross-account
```
## Security Best Practices
### Principle of Least Privilege [[principle-of-least-privilege|POLP]]
Always grant the minimum permissions necessary for the task. Use condition keys to further restrict access:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mybucket/*",
            "Condition": {
                "DateLessThan": {
                    "aws:CurrentTime": "2023-12-31T23:59:59Z"
                }
            }
        }
    ]
}
```

### External ID for Enhanced Security

When allowing third parties to assume roles, use external IDs:

```bash
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/ThirdPartyRole \
    --role-session-name ThirdPartySession \
    --external-id UniqueExternalIdentifier123
```

### Session Duration Management

Configure appropriate session durations based on use case:

```bash
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/MyRole \
    --role-session-name MySession \
    --duration-seconds 3600  # 1 hour
```

## Integration Examples

### EC2 Instance Roles
EC2 instances can automatically assume roles without storing credentials:
```bash
# Inside EC2 instance
aws sts get-caller-identity
# Returns the role assigned to the instance
```
### Lambda Function Execution
Lambda functions automatically receive temporary credentials:

```python
import boto3

def lambda_handler(event, context):
    sts_client = boto3.client('sts')
    identity = sts_client.get_caller_identity()
    return {
        'statusCode': 200,
        'body': f"Function running as: {identity['Arn']}"
    }
```
### CI/CD Pipeline Integration
Use role assumption in deployment pipelines:
```bash
# In CI/CD script
TEMP_CREDS=$(aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/DeploymentRole \
    --role-session-name "Pipeline-$(date +%s)" \
    --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
    --output text)

export AWS_ACCESS_KEY_ID=$(echo $TEMP_CREDS | cut -d' ' -f1)
export AWS_SECRET_ACCESS_KEY=$(echo $TEMP_CREDS | cut -d' ' -f2)
export AWS_SESSION_TOKEN=$(echo $TEMP_CREDS | cut -d' ' -f3)

# Now perform deployment actions
aws s3 sync ./build s3://deployment-bucket/
```

## Troubleshooting Common Issues

### Access Denied Errors

Check trust relationships and ensure the assuming entity has permission to assume the role:

```bash
aws sts get-caller-identity
aws iam get-role --role-name MyRole
```

### Token Expiration

Monitor token expiration and implement refresh logic:

```bash
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/MyRole \
    --role-session-name MySession \
    --query 'Credentials.Expiration' \
    --output text
```

### MFA Requirements

When MFA is required, include the MFA device and token:

```bash
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/MFARole \
    --role-session-name MFASession \
    --serial-number arn:aws:iam::123456789012:mfa/username \
    --token-code 123456
```

AWS STS provides the foundation for secure, temporary access to AWS resources, enabling sophisticated authentication and authorization patterns while maintaining the principle of least privilege and supporting various integration scenarios.
