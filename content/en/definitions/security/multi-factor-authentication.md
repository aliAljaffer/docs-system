---
title: multi factor authentication
category: Security
description: In AWS IAM, MFA is the best practice that requires a second authentication
  factor on top of a password. It helps verify that the logging-in user is who they
  say they are. You can enable MFA for root a
tags:
- cloud
- fundamentals
- security
---


# multi factor authentication

`cloud` `fundamentals` `security`

In [[security-user-and-identity-management|AWS IAM]], MFA is the best practice that requires a second authentication factor on top of a password. It helps verify that the logging-in user is who they say they are. You can enable MFA for root and [[security-user-and-identity-management|IAM]] users you created in your account.

### Methods for MFA:

#### Passkeys and security keys
Passkeys are created in password managers such as Google Password Manager, iCloud KeyChain, 1Password, etc. using biometric/device PIN data to allow users to sign in into AWS.

#### Virtual Authenticator Apps
These apps implement time-based one-time passwords ([[totp|TOTP]]) and support multiple tokens for different log-in portals on a single device. Virtual authennticators are supported for IAM users in teh AWS GovCloud (US)  [[region|regions]] and other AWS [[region|regions]].

#### Hardware TOTP
These are hardware devices provided by Thales. These tokens are for use exclusively with AWS accounts.

#### Hardware TOTP for AWS GovCloud Regions
See . Same but for secure government regions.
