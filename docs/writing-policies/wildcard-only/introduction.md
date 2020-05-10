
Wildcard-only section
---------------------

You'll notice that as of release 0.7.1, there is a new section for `wildcard-only`:

```yaml
mode: crud
name: myRole
# Specify resource ARNs
read:
- ''
# Actions that do not support resource constraints
wildcard-only:
  single-actions: # standalone actions
  - ''
  # Service-wide, per access level - like 's3' or 'ec2'
  service-read:
  - ''
  service-write:
  - ''
  service-list:
  - ''
  service-tagging:
  - ''
  service-permissions-management:
  - ''
```

The wildcard-only section is meant to hold IAM actions that do not support resource constraints. Most IAM actions do support resource constraints - for instance, `s3:GetObject` can be restricted according to a specific object or path within an S3 bucket ARN , like `arn:aws:s3:::mybucket/path/*`. However, some IAM actions do **not** support resource constraints.

### Example

For example, run a query against the IAM database to determine "which S3 actions at the LIST access level do not support resource constraints":

```bash
policy_sentry query action-table --service s3 --access-level list --wildcard-only
```

The output will be:

```text
 s3 LIST actions that must use wildcards in the resources block:
 [
     "s3:ListAllMyBuckets"
 ]}
```

Similarly, S3 has a few actions that at the "Read" access level that do not support resource constraints. Run this query against the IAM database to discover those actions:

```bash
policy_sentry query action-table --service s3 --access-level read --wildcard-only
```

The output will be:

```text
s3 READ actions that must use wildcards in the resources block:
[
    "s3:GetAccessPoint",
    "s3:GetAccountPublicAccessBlock",
    "s3:ListAccessPoints"
]
```
