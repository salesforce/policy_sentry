Action table
============

```bash
# NOTE: Use --fmt yaml or --fmt json to change the output format. Defaults to json for querying

# Get a list of actions that do not support resource constraints
policy_sentry query action-table --service s3 --resource-type '*' --fmt yaml

# Get a list of actions at the "Read" level in S3 that do not support resource constraints
policy_sentry query action-table --service s3 --access-level read --resource-type '*' --fmt yaml

# Get a list of actions at the "Write" level in SSM service for resource type "parameter"
policy_sentry query action-table --service ssm --access-level write --resource-type parameter

# Get a list of all IAM Actions available to the RAM service
policy_sentry query action-table --service ram

# Get details about the `ram:TagResource` IAM Action
policy_sentry query action-table --service ram --name tagresource

# Get a list of all IAM actions under the RAM service that have the Permissions management access level.
policy_sentry query action-table --service ram --access-level permissions-management

# Get a list of all IAM actions under the SES service that support the `ses:FeedbackAddress` condition key.
policy_sentry query action-table --service ses --condition ses:FeedbackAddress

```

Options
-------

```text
Usage: policy_sentry query action-table [OPTIONS]

Options:
  --service TEXT                  Filter according to AWS service.  [required]
  --name TEXT                     The name of IAM Action. For example, if the
                                  action is "iam:ListUsers", supply
                                  "ListUsers" here.
  --access-level [read|write|list|tagging|permissions-management]
                                  If action table is chosen, you can use this
                                  to filter according to CRUD levels.
                                  Acceptable values are read, write, list,
                                  tagging, permissions-management
  --condition TEXT                If action table is chosen, you can supply a
                                  condition key to show a list of all IAM
                                  actions that support the condition key.
  --resource-type TEXT            Supply a resource type to show a list of all
                                  IAM actions that support the resource type.
  --fmt [yaml|json]               Format output as YAML or JSON. Defaults to
                                  "yaml"
  --v                             Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO
  --help                          Show this message and exit.
```


## Examples

###  Get a list of all services in the database

<details open>
<summary>policy_sentry query action-table --service all</summary>
<br>
<pre>
<code>
All services in the database:

a4b
access-analyzer
account
acm
acm-pca
amplify
apigateway
appconfig
appflow
application-autoscaling
applicationinsights
appmesh
appmesh-preview
appstream
appsync
arsenal
artifact
athena
autoscaling
autoscaling-plans
aws-marketplace
aws-marketplace-management
aws-portal
awsconnector
backup
backup-storage
batch
budgets
cassandra
ce
chatbot
chime
cloud9
clouddirectory
cloudformation
cloudfront
cloudhsm
cloudsearch
cloudtrail
cloudwatch
codeartifact
codebuild
codecommit
codedeploy
codeguru
codeguru-profiler
codeguru-reviewer
codepipeline
codestar
codestar-connections
codestar-notifications
cognito-identity
cognito-idp
cognito-sync
comprehend
comprehendmedical
compute-optimizer
config
connect
cur
dataexchange
datapipeline
datasync
dax
dbqms
deepcomposer
deeplens
deepracer
detective
devicefarm
directconnect
discovery
dlm
dms
ds
dynamodb
ebs
ec2
ec2-instance-connect
ec2messages
ecr
ecs
eks
elastic-inference
elasticache
elasticbeanstalk
elasticfilesystem
elasticloadbalancing
elasticmapreduce
elastictranscoder
es
events
execute-api
firehose
fms
forecast
frauddetector
freertos
fsx
gamelift
glacier
globalaccelerator
glue
greengrass
groundstation
groundtruthlabeling
guardduty
health
iam
imagebuilder
importexport
inspector
iot
iot-device-tester
iot1click
iotanalytics
iotevents
iotsitewise
iotthingsgraph
iq
iq-permission
kafka
kendra
kinesis
kinesisanalytics
kinesisvideo
kms
lakeformation
lambda
launchwizard
lex
license-manager
lightsail
logs
machinelearning
macie
macie2
managedblockchain
mechanicalturk
mediaconnect
mediaconvert
medialive
mediapackage
mediapackage-vod
mediastore
mediatailor
mgh
mobileanalytics
mobilehub
mobiletargeting
mq
neptune-db
networkmanager
opsworks
opsworks-cm
organizations
outposts
personalize
pi
polly
pricing
purchase-orders
qldb
quicksight
ram
rds
rds-data
rds-db
redshift
rekognition
resource-explorer
resource-groups
robomaker
route53
route53domains
route53resolver
s3
sagemaker
savingsplans
schemas
sdb
secretsmanager
securityhub
serverlessrepo
servicecatalog
servicediscovery
servicequotas
ses
shield
signer
sms
sms-voice
snowball
sns
sqs
ssm
ssmmessages
sso
sso-directory
states
storagegateway
sts
sumerian
support
swf
synthetics
tag
textract
transcribe
transfer
translate
trustedadvisor
waf
waf-regional
wafv2
wam
wellarchitected
workdocs
worklink
workmail
workmailmessageflow
workspaces
xray
</code>
</pre>
</details>


### Actions on all services at a specific Access Level
<details open>
<summary>policy_sentry query action-table --service all --access-level permissions-management</summary>
<br>
<pre>
<code>
permissions-management actions across ALL services:
acm-pca:CreatePermission
acm-pca:DeletePermission
apigateway:UpdateRestApiPolicy
backup:DeleteBackupVaultAccessPolicy
backup:PutBackupVaultAccessPolicy
chime:DeleteVoiceConnectorTerminationCredentials
chime:PutVoiceConnectorTerminationCredentials
cloudformation:SetStackPolicy
cloudsearch:UpdateServiceAccessPolicies
codeartifact:DeleteDomainPermissionsPolicy
codeartifact:DeleteRepositoryPermissionsPolicy
codebuild:DeleteResourcePolicy
codebuild:DeleteSourceCredentials
codebuild:ImportSourceCredentials
codebuild:PutResourcePolicy
codeguru-profiler:PutPermission
codeguru-profiler:RemovePermission
codestar:AssociateTeamMember
codestar:CreateProject
codestar:DeleteProject
codestar:DisassociateTeamMember
codestar:UpdateTeamMember
cognito-identity:CreateIdentityPool
cognito-identity:DeleteIdentities
cognito-identity:DeleteIdentityPool
cognito-identity:GetId
cognito-identity:MergeDeveloperIdentities
cognito-identity:SetIdentityPoolRoles
cognito-identity:UnlinkDeveloperIdentity
cognito-identity:UnlinkIdentity
cognito-identity:UpdateIdentityPool
deeplens:AssociateServiceRoleToAccount
ds:CreateConditionalForwarder
ds:CreateDirectory
ds:CreateMicrosoftAD
ds:CreateTrust
ds:ShareDirectory
ec2:CreateNetworkInterfacePermission
ec2:DeleteNetworkInterfacePermission
ec2:ModifySnapshotAttribute
ec2:ModifyVpcEndpointServicePermissions
ec2:ResetSnapshotAttribute
ecr:DeleteRepositoryPolicy
ecr:SetRepositoryPolicy
elasticfilesystem:DeleteFileSystemPolicy
elasticfilesystem:PutFileSystemPolicy
elasticmapreduce:PutBlockPublicAccessConfiguration
es:CreateElasticsearchDomain
es:UpdateElasticsearchDomainConfig
glacier:AbortVaultLock
glacier:CompleteVaultLock
glacier:DeleteVaultAccessPolicy
glacier:InitiateVaultLock
glacier:SetDataRetrievalPolicy
glacier:SetVaultAccessPolicy
glue:DeleteResourcePolicy
glue:PutResourcePolicy
greengrass:AssociateServiceRoleToAccount
health:DisableHealthServiceAccessForOrganization
health:EnableHealthServiceAccessForOrganization
iam:AddClientIDToOpenIDConnectProvider
iam:AddRoleToInstanceProfile
iam:AddUserToGroup
iam:AttachGroupPolicy
iam:AttachRolePolicy
iam:AttachUserPolicy
iam:ChangePassword
iam:CreateAccessKey
iam:CreateAccountAlias
iam:CreateGroup
iam:CreateInstanceProfile
iam:CreateLoginProfile
iam:CreateOpenIDConnectProvider
iam:CreatePolicy
iam:CreatePolicyVersion
iam:CreateRole
iam:CreateSAMLProvider
iam:CreateServiceLinkedRole
iam:CreateServiceSpecificCredential
iam:CreateUser
iam:CreateVirtualMFADevice
iam:DeactivateMFADevice
iam:DeleteAccessKey
iam:DeleteAccountAlias
iam:DeleteAccountPasswordPolicy
iam:DeleteGroup
iam:DeleteGroupPolicy
iam:DeleteInstanceProfile
iam:DeleteLoginProfile
iam:DeleteOpenIDConnectProvider
iam:DeletePolicy
iam:DeletePolicyVersion
iam:DeleteRole
iam:DeleteRolePermissionsBoundary
iam:DeleteRolePolicy
iam:DeleteSAMLProvider
iam:DeleteSSHPublicKey
iam:DeleteServerCertificate
iam:DeleteServiceLinkedRole
iam:DeleteServiceSpecificCredential
iam:DeleteSigningCertificate
iam:DeleteUser
iam:DeleteUserPermissionsBoundary
iam:DeleteUserPolicy
iam:DeleteVirtualMFADevice
iam:DetachGroupPolicy
iam:DetachRolePolicy
iam:DetachUserPolicy
iam:EnableMFADevice
iam:PassRole
iam:PutGroupPolicy
iam:PutRolePermissionsBoundary
iam:PutRolePolicy
iam:PutUserPermissionsBoundary
iam:PutUserPolicy
iam:RemoveClientIDFromOpenIDConnectProvider
iam:RemoveRoleFromInstanceProfile
iam:RemoveUserFromGroup
iam:ResetServiceSpecificCredential
iam:ResyncMFADevice
iam:SetDefaultPolicyVersion
iam:SetSecurityTokenServicePreferences
iam:UpdateAccessKey
iam:UpdateAccountPasswordPolicy
iam:UpdateAssumeRolePolicy
iam:UpdateGroup
iam:UpdateLoginProfile
iam:UpdateOpenIDConnectProviderThumbprint
iam:UpdateRole
iam:UpdateRoleDescription
iam:UpdateSAMLProvider
iam:UpdateSSHPublicKey
iam:UpdateServerCertificate
iam:UpdateServiceSpecificCredential
iam:UpdateSigningCertificate
iam:UpdateUser
iam:UploadSSHPublicKey
iam:UploadServerCertificate
iam:UploadSigningCertificate
imagebuilder:PutComponentPolicy
imagebuilder:PutImagePolicy
imagebuilder:PutImageRecipePolicy
iot:AttachPolicy
iot:AttachPrincipalPolicy
iot:DetachPolicy
iot:DetachPrincipalPolicy
iot:SetDefaultAuthorizer
iot:SetDefaultPolicyVersion
iotsitewise:CreateAccessPolicy
iotsitewise:DeleteAccessPolicy
iotsitewise:UpdateAccessPolicy
kms:CreateGrant
kms:PutKeyPolicy
kms:RetireGrant
kms:RevokeGrant
lakeformation:BatchGrantPermissions
lakeformation:BatchRevokePermissions
lakeformation:GrantPermissions
lakeformation:PutDataLakeSettings
lakeformation:RevokePermissions
lambda:AddLayerVersionPermission
lambda:AddPermission
lambda:DisableReplication
lambda:EnableReplication
lambda:RemoveLayerVersionPermission
lambda:RemovePermission
license-manager:UpdateServiceSettings
lightsail:GetRelationalDatabaseMasterUserPassword
logs:DeleteResourcePolicy
logs:PutResourcePolicy
mediapackage:RotateIngestEndpointCredentials
mediastore:DeleteContainerPolicy
mediastore:PutContainerPolicy
opsworks:SetPermission
opsworks:UpdateUserProfile
quicksight:CreateAdmin
quicksight:CreateGroup
quicksight:CreateGroupMembership
quicksight:CreateIAMPolicyAssignment
quicksight:CreateUser
quicksight:DeleteGroup
quicksight:DeleteGroupMembership
quicksight:DeleteIAMPolicyAssignment
quicksight:DeleteUser
quicksight:DeleteUserByPrincipalId
quicksight:RegisterUser
quicksight:UpdateDashboardPermissions
quicksight:UpdateGroup
quicksight:UpdateIAMPolicyAssignment
quicksight:UpdateTemplatePermissions
quicksight:UpdateUser
ram:AcceptResourceShareInvitation
ram:AssociateResourceShare
ram:CreateResourceShare
ram:DeleteResourceShare
ram:DisassociateResourceShare
ram:EnableSharingWithAwsOrganization
ram:RejectResourceShareInvitation
ram:UpdateResourceShare
rds:AuthorizeDBSecurityGroupIngress
rds-db:connect
redshift:AuthorizeSnapshotAccess
redshift:CreateClusterUser
redshift:CreateSnapshotCopyGrant
redshift:JoinGroup
redshift:ModifyClusterIamRoles
redshift:RevokeSnapshotAccess
route53resolver:PutResolverRulePolicy
s3:BypassGovernanceRetention
s3:DeleteAccessPointPolicy
s3:DeleteBucketPolicy
s3:ObjectOwnerOverrideToBucketOwner
s3:PutAccessPointPolicy
s3:PutAccountPublicAccessBlock
s3:PutBucketAcl
s3:PutBucketPolicy
s3:PutBucketPublicAccessBlock
s3:PutObjectAcl
s3:PutObjectVersionAcl
secretsmanager:DeleteResourcePolicy
secretsmanager:PutResourcePolicy
servicecatalog:CreatePortfolioShare
servicecatalog:DeletePortfolioShare
sns:AddPermission
sns:CreateTopic
sns:RemovePermission
sns:SetTopicAttributes
sqs:AddPermission
sqs:CreateQueue
sqs:RemovePermission
sqs:SetQueueAttributes
ssm:ModifyDocumentPermission
sso:AssociateDirectory
sso:AssociateProfile
sso:CreateApplicationInstance
sso:CreateApplicationInstanceCertificate
sso:CreatePermissionSet
sso:CreateProfile
sso:CreateTrust
sso:DeleteApplicationInstance
sso:DeleteApplicationInstanceCertificate
sso:DeletePermissionSet
sso:DeletePermissionsPolicy
sso:DeleteProfile
sso:DisassociateDirectory
sso:DisassociateProfile
sso:ImportApplicationInstanceServiceProviderMetadata
sso:PutPermissionsPolicy
sso:StartSSO
sso:UpdateApplicationInstanceActiveCertificate
sso:UpdateApplicationInstanceDisplayData
sso:UpdateApplicationInstanceResponseConfiguration
sso:UpdateApplicationInstanceResponseSchemaConfiguration
sso:UpdateApplicationInstanceSecurityConfiguration
sso:UpdateApplicationInstanceServiceProviderConfiguration
sso:UpdateApplicationInstanceStatus
sso:UpdateDirectoryAssociation
sso:UpdatePermissionSet
sso:UpdateProfile
sso:UpdateSSOConfiguration
sso:UpdateTrust
sso-directory:AddMemberToGroup
sso-directory:CreateAlias
sso-directory:CreateGroup
sso-directory:CreateUser
sso-directory:DeleteGroup
sso-directory:DeleteUser
sso-directory:DisableUser
sso-directory:EnableUser
sso-directory:RemoveMemberFromGroup
sso-directory:UpdateGroup
sso-directory:UpdatePassword
sso-directory:UpdateUser
sso-directory:VerifyEmail
storagegateway:DeleteChapCredentials
storagegateway:SetLocalConsolePassword
storagegateway:SetSMBGuestPassword
storagegateway:UpdateChapCredentials
waf:DeletePermissionPolicy
waf:PutPermissionPolicy
waf-regional:DeletePermissionPolicy
waf-regional:PutPermissionPolicy
wafv2:CreateWebACL
wafv2:DeletePermissionPolicy
wafv2:DeleteWebACL
wafv2:PutPermissionPolicy
wafv2:UpdateWebACL
worklink:UpdateDevicePolicyConfiguration
workmail:ResetPassword
workmail:ResetUserPassword
xray:PutEncryptionConfig
</code>
</pre>
</details>


### All IAM actions under a specific service that have a specific access level

<details open>
<summary>policy_sentry query action-table --service s3 --access-level permissions-management</summary>
<br>
<pre>
<code>
All IAM actions under the s3 service that have the access level permissions-management:
[
    "s3:BypassGovernanceRetention",
    "s3:DeleteAccessPointPolicy",
    "s3:DeleteBucketPolicy",
    "s3:ObjectOwnerOverrideToBucketOwner",
    "s3:PutAccessPointPolicy",
    "s3:PutAccountPublicAccessBlock",
    "s3:PutBucketAcl",
    "s3:PutBucketPolicy",
    "s3:PutBucketPublicAccessBlock",
    "s3:PutObjectAcl",
    "s3:PutObjectVersionAcl"
]
</code>
</pre>
</details>


### Actions for S3 service at Write access level that only support wildcard resources (*)

<details open>
<summary>policy_sentry query action-table --service s3 --access-level read --resource-type '*' --fmt yaml</summary>
<br>
<pre>
<code>
s3 READ actions that must use wildcards in the resources block:
- s3:GetAccessPoint
- s3:GetAccountPublicAccessBlock
- s3:ListAccessPoints
- s3:ListJobs
</code>
</pre>
</details>

### Actions for S3 service at any access level that only support wildcard resources (*)

<details open>
<summary>policy_sentry query action-table --service s3 --resource-type '*' --fmt yaml</summary>
<br>
<pre>
<code>
IAM actions under s3 service that support wildcard resource values only:
- s3:CreateJob
- s3:GetAccessPoint
- s3:GetAccountPublicAccessBlock
- s3:ListAccessPoints
- s3:ListAllMyBuckets
- s3:ListJobs
- s3:PutAccountPublicAccessBlock
</code>
</pre>
</details>


### Get a list of all IAM actions under the service that support the specified condition key

<details open>
<summary>policy_sentry query action-table --service ses --condition ses:FeedbackAddress</summary>
<br>
<pre>
<code>
IAM actions under ses service that support the ses:FeedbackAddress condition only:
[
    "ses:SendEmail"
]
</code>
</pre>
</details>


### Get data about a specific action


<details open>
<summary>policy_sentry query action-table --service s3 --name GetObject</summary>
<br>
<pre>
<code>
{
    "s3": [
        {
            "action": "s3:GetObject",
            "description": "Retrieves objects from Amazon S3.",
            "access_level": "Read",
            "resource_arn_format": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "condition_keys": [],
            "dependent_actions": []
        },
        {
            "action": "s3:GetObject",
            "description": "Retrieves objects from Amazon S3.",
            "access_level": "Read",
            "resource_arn_format": "*",
            "condition_keys": [],
            "dependent_actions": []
        }
    ]
}
</code>
</pre>
</details>

### Get a list of all IAM Actions available to the service

<details open>
<summary>policy_sentry query action-table --service cloud9</summary>
<br>
<pre>
<code>
ALL cloud9 actions:
cloud9:CreateEnvironmentEC2
cloud9:CreateEnvironmentMembership
cloud9:DeleteEnvironment
cloud9:DeleteEnvironmentMembership
cloud9:DescribeEnvironmentMemberships
cloud9:DescribeEnvironmentStatus
cloud9:DescribeEnvironments
cloud9:GetUserSettings
cloud9:ListEnvironments
cloud9:ListTagsForResource
cloud9:TagResource
cloud9:UntagResource
cloud9:UpdateEnvironment
cloud9:UpdateEnvironmentMembership
cloud9:UpdateUserSettings
</code>
</pre>
</details>
