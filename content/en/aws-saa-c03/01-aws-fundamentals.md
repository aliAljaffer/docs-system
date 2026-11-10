# 1. AWS Fundamentals

**Goal:** Choose a region and understand how AWS places its infrastructure.

## Regions

Use these criteria to choose an [[region|AWS Region]]:

1. Compliance with data governance and legal requirements. Data never leaves a region without explicit permission.
2. Proximity to customers.
3. Services available in the region.
4. Pricing.

The Region Table shows which services each region offers.

## Availability Zones

Many services use [[availability-zones|Availability Zones]] (AZs) to add resilience. Examples in this course:

- RDS Multi-AZ uses a synchronous standby.
- Aurora stores six copies of data across three AZs.
- Cross-zone load balancing spreads traffic across AZs.

## Edge locations

[[edge-location|Edge locations]] sit close to users. These services use them:

| Service | Role at the edge |
|---|---|
| [[networking-cloudfront|CloudFront]] | Caches content at edge locations |
| Global Accelerator | Routes connections through edge locations to your app |
| [[compute-lambda|Lambda]]@Edge | Runs code close to users |

## Exam tips

- Data stays in its region unless you allow otherwise.
- Check the Region Table before you choose a region for a service.
- Pricing is one of four criteria. Compare it with compliance and proximity.

[Next: IAM and Accounts](02-iam-and-accounts.md)
