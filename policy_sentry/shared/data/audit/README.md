# Audit files

1. Resource exposure access level: These are IAM actions that meet one of the following criteria:
  - Actions classified at "Permissions management" access level
  - Actions under "IAM" service at the "Write" access level
  - (We should add RAM service at the "Write" access level to this)
2. Privilege escalation:
  - Based on Rhino Security Labs research [here](https://github.com/RhinoSecurityLabs/Cloud-Security-Research/blob/master/AWS/aws_escalate/aws_escalate.py#L247)
  

### Roadmap

In the future, we will add these as well:
* Network exposure (Public IPs, security groups)
* Data access (as opposed to config access).
  - We can identify these policies based on the actions that are associated with different ARN types. For instance, S3 bucket object ARN permits data access, whereas S3 bucket ARN or S3 job ARN permits config access
