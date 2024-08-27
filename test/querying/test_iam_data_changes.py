import unittest
import json
from policy_sentry.querying.all import get_all_actions
from policy_sentry.querying.actions import get_actions_for_service
from policy_sentry.querying.arns import get_arn_types_for_service


class IAMDefinitionQA(unittest.TestCase):
    def setUp(self) -> None:
        all_actions = get_all_actions()
        self.all_actions = list(all_actions)
        self.all_actions.sort()

    def test_services_with_multiple_pages_apigateway(self):
        """Ensure that apigateway v1 and apigateway v2 actions are both present in the ses namespace"""
        # API Gateway Management V1: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonapigatewaymanagement.html
        self.assertTrue("apigateway:AddCertificateToDomain" in self.all_actions)
        self.assertTrue("apigateway:RemoveCertificateFromDomain" in self.all_actions)
        self.assertTrue("apigateway:SetWebACL" in self.all_actions)
        # API Gateway Management V2: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonapigatewaymanagement.html
        # API Gateway V2 doesn't have any unique actions in but it does have some unique resource types. Let's make sure those resource types are in the IAM Definition.
        # Resource types unique to API Gateway V2:
        resource_types = get_arn_types_for_service("apigateway")
        resource_types = list(resource_types.keys())
        self.assertTrue("AccessLogSettings" in resource_types)
        # Resource types unique to API Gateway V1:
        self.assertTrue("RestApi" in resource_types)

    def test_services_with_multiple_pages_aws_marketplace(self):
        """Ensure that aws-marketplace actions from all the different aws-marketplace SAR pages are present in the IAM definition."""
        # Overlap: AWS Marketplace, Marketplace Catalog, and AWS Marketplace Entitlement service, AWS Marketplace Image Building Service, AWS Marketplace Metering Service, AWS Marketplace Private Marketplace, and AWS Marketplace Procurement Systems
        # AWS Marketplace: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplace.html
        self.assertTrue("aws-marketplace:AcceptAgreementApprovalRequest" in self.all_actions)
        # AWS Marketplace Catalog: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplacecatalog.html
        self.assertTrue("aws-marketplace:CancelChangeSet" in self.all_actions)
        # AWS Marketplace Entitlement Service: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplaceentitlementservice.html
        self.assertTrue("aws-marketplace:GetEntitlements" in self.all_actions)
        # AWS Marketplace Image Building Service: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplaceimagebuildingservice.html
        self.assertTrue("aws-marketplace:DescribeBuilds" in self.all_actions)
        # AWS Marketplace Metering Service: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplacemeteringservice.html
        self.assertTrue("aws-marketplace:BatchMeterUsage" in self.all_actions)
        # AWS Marketplace Private Marketplace: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplaceprivatemarketplace.html
        self.assertTrue("aws-marketplace:AssociateProductsWithPrivateMarketplace" in self.all_actions)
        # AWS Marketplace Procurement Systems: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsmarketplaceprocurementsystemsintegration.html
        self.assertTrue("aws-marketplace:DescribeProcurementSystemConfiguration" in self.all_actions)

        results = get_actions_for_service("aws-marketplace")
        actions = [
            "aws-marketplace:AcceptAgreementApprovalRequest",
            "aws-marketplace:BatchMeterUsage",
            "aws-marketplace:CancelAgreementRequest",
            "aws-marketplace:CancelChangeSet",
            "aws-marketplace:CompleteTask",
            "aws-marketplace:DescribeAgreement",
            "aws-marketplace:DescribeBuilds",
            "aws-marketplace:DescribeChangeSet",
            "aws-marketplace:DescribeEntity",
            "aws-marketplace:DescribeProcurementSystemConfiguration",
            "aws-marketplace:DescribeTask",
            "aws-marketplace:GetAgreementApprovalRequest",
            "aws-marketplace:GetAgreementRequest",
            "aws-marketplace:GetAgreementTerms",
            "aws-marketplace:GetEntitlements",
            "aws-marketplace:ListAgreementApprovalRequests",
            "aws-marketplace:ListAgreementRequests",
            "aws-marketplace:ListBuilds",
            "aws-marketplace:ListChangeSets",
            "aws-marketplace:ListEntities",
            "aws-marketplace:ListTasks",
            "aws-marketplace:MeterUsage",
            "aws-marketplace:PutProcurementSystemConfiguration",
            "aws-marketplace:RegisterUsage",
            "aws-marketplace:RejectAgreementApprovalRequest",
            "aws-marketplace:ResolveCustomer",
            "aws-marketplace:SearchAgreements",
            "aws-marketplace:StartBuild",
            "aws-marketplace:StartChangeSet",
            "aws-marketplace:Subscribe",
            "aws-marketplace:Unsubscribe",
            "aws-marketplace:UpdateAgreementApprovalRequest",
            "aws-marketplace:UpdateTask",
            "aws-marketplace:ViewSubscriptions",
        ]
        for action in actions:
            self.assertTrue(action in results)

    def test_services_with_multiple_pages_greengrass(self):
        """Ensure that greengrass v1 and greengrass v2 actions are both present in the greengrass namespace"""
        # Greengrass V1: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiotgreengrass.html
        self.assertTrue("greengrass:CreateResourceDefinition" in self.all_actions)
        # Greengrass V2: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiotgreengrassv2.html
        self.assertTrue("greengrass:CreateComponentVersion" in self.all_actions)
        results = get_actions_for_service("greengrass")
        actions = [
            "greengrass:AssociateRoleToGroup",
            "greengrass:CreateConnectorDefinition",
            "greengrass:CreateConnectorDefinitionVersion",
            "greengrass:CreateCoreDefinition",
            "greengrass:CreateCoreDefinitionVersion",
            "greengrass:CreateDeviceDefinition",
            "greengrass:CreateDeviceDefinitionVersion",
            "greengrass:CreateFunctionDefinition",
            "greengrass:CreateFunctionDefinitionVersion",
            "greengrass:CreateGroup",
            "greengrass:CreateGroupCertificateAuthority",
            "greengrass:CreateGroupVersion",
            "greengrass:CreateLoggerDefinition",
            "greengrass:CreateLoggerDefinitionVersion",
            "greengrass:CreateResourceDefinition",
            "greengrass:CreateResourceDefinitionVersion",
            "greengrass:CreateSoftwareUpdateJob",
            "greengrass:CreateSubscriptionDefinition",
            "greengrass:CreateSubscriptionDefinitionVersion",
            "greengrass:DeleteConnectorDefinition",
            "greengrass:DeleteCoreDefinition",
            "greengrass:DeleteDeviceDefinition",
            "greengrass:DeleteFunctionDefinition",
            "greengrass:DeleteGroup",
            "greengrass:DeleteLoggerDefinition",
            "greengrass:DeleteResourceDefinition",
            "greengrass:DeleteSubscriptionDefinition",
            "greengrass:DisassociateRoleFromGroup",
            "greengrass:Discover",
            "greengrass:GetAssociatedRole",
            "greengrass:GetBulkDeploymentStatus",
            "greengrass:GetConnectorDefinition",
            "greengrass:GetConnectorDefinitionVersion",
            "greengrass:GetCoreDefinition",
            "greengrass:GetCoreDefinitionVersion",
            "greengrass:GetDeploymentStatus",
            "greengrass:GetDeviceDefinition",
            "greengrass:GetDeviceDefinitionVersion",
            "greengrass:GetFunctionDefinition",
            "greengrass:GetFunctionDefinitionVersion",
            "greengrass:GetGroup",
            "greengrass:GetGroupCertificateAuthority",
            "greengrass:GetGroupCertificateConfiguration",
            "greengrass:GetGroupVersion",
            "greengrass:GetLoggerDefinition",
            "greengrass:GetLoggerDefinitionVersion",
            "greengrass:GetResourceDefinition",
            "greengrass:GetResourceDefinitionVersion",
            "greengrass:GetSubscriptionDefinition",
            "greengrass:GetSubscriptionDefinitionVersion",
            "greengrass:GetThingRuntimeConfiguration",
            "greengrass:ListBulkDeploymentDetailedReports",
            "greengrass:ListBulkDeployments",
            "greengrass:ListConnectorDefinitionVersions",
            "greengrass:ListConnectorDefinitions",
            "greengrass:ListCoreDefinitionVersions",
            "greengrass:ListCoreDefinitions",
            "greengrass:ListDeviceDefinitionVersions",
            "greengrass:ListDeviceDefinitions",
            "greengrass:ListFunctionDefinitionVersions",
            "greengrass:ListFunctionDefinitions",
            "greengrass:ListGroupCertificateAuthorities",
            "greengrass:ListGroupVersions",
            "greengrass:ListGroups",
            "greengrass:ListLoggerDefinitionVersions",
            "greengrass:ListLoggerDefinitions",
            "greengrass:ListResourceDefinitionVersions",
            "greengrass:ListResourceDefinitions",
            "greengrass:ListSubscriptionDefinitionVersions",
            "greengrass:ListSubscriptionDefinitions",
            "greengrass:ResetDeployments",
            "greengrass:StartBulkDeployment",
            "greengrass:StopBulkDeployment",
            "greengrass:UpdateConnectorDefinition",
            "greengrass:UpdateCoreDefinition",
            "greengrass:UpdateDeviceDefinition",
            "greengrass:UpdateFunctionDefinition",
            "greengrass:UpdateGroup",
            "greengrass:UpdateGroupCertificateConfiguration",
            "greengrass:UpdateLoggerDefinition",
            "greengrass:UpdateResourceDefinition",
            "greengrass:UpdateSubscriptionDefinition",
            "greengrass:UpdateThingRuntimeConfiguration",
        ]
        for action in actions:
            self.assertTrue(action in results)
            # if action not in results:
            #     print(action)

    def test_services_with_multiple_pages_elb(self):
        """Ensure that elb v1 and elb v2 actions are both present in the elasticloadbalancing namespace"""
        results = get_actions_for_service("elasticloadbalancing")
        actions = [
            "elasticloadbalancing:ApplySecurityGroupsToLoadBalancer",
            "elasticloadbalancing:AttachLoadBalancerToSubnets",
            "elasticloadbalancing:ConfigureHealthCheck",
            "elasticloadbalancing:CreateAppCookieStickinessPolicy",
            "elasticloadbalancing:CreateLBCookieStickinessPolicy",
            "elasticloadbalancing:CreateLoadBalancerListeners",
            "elasticloadbalancing:CreateLoadBalancerPolicy",
            "elasticloadbalancing:DeleteLoadBalancerListeners",
            "elasticloadbalancing:DeleteLoadBalancerPolicy",
            "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
            "elasticloadbalancing:DescribeInstanceHealth",
            "elasticloadbalancing:DescribeLoadBalancerPolicies",
            "elasticloadbalancing:DescribeLoadBalancerPolicyTypes",
            "elasticloadbalancing:DetachLoadBalancerFromSubnets",
            "elasticloadbalancing:DisableAvailabilityZonesForLoadBalancer",
            "elasticloadbalancing:EnableAvailabilityZonesForLoadBalancer",
            "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
            "elasticloadbalancing:SetLoadBalancerListenerSSLCertificate",
            "elasticloadbalancing:SetLoadBalancerPoliciesForBackendServer",
            "elasticloadbalancing:SetLoadBalancerPoliciesOfListener",
        ]
        for action in actions:
            self.assertTrue(action in results)

    def test_services_with_multiple_pages_lex(self):
        """Ensure that lex v1 and lex v2 actions are both present in the lex namespace"""
        # Lex V1: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlex.html
        self.assertTrue("lex:DeleteUtterances" in self.all_actions)
        # Lex V2: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlexv2.html
        self.assertTrue("lex:ListBotLocales" in self.all_actions)
        results = get_actions_for_service("lex")
        actions = [
            "lex:CreateIntentVersion",
            "lex:CreateSlotTypeVersion",
            "lex:DeleteBotChannelAssociation",
            "lex:DeleteIntentVersion",
            "lex:DeleteSlotTypeVersion",
            "lex:GetBot",
            "lex:GetBotAlias",
            "lex:GetBotAliases",
            "lex:GetBotChannelAssociation",
            "lex:GetBotChannelAssociations",
            "lex:GetBotVersions",
            "lex:GetBots",
            "lex:GetBuiltinIntent",
            "lex:GetBuiltinIntents",
            "lex:GetBuiltinSlotTypes",
            "lex:GetExport",
            "lex:GetImport",
            "lex:GetIntent",
            "lex:GetIntentVersions",
            "lex:GetIntents",
            "lex:GetMigration",
            "lex:GetMigrations",
            "lex:GetSlotType",
            "lex:GetSlotTypeVersions",
            "lex:GetSlotTypes",
            "lex:GetUtterancesView",
            "lex:PostContent",
            "lex:PostText",
            "lex:PutBot",
            "lex:PutBotAlias",
            "lex:PutIntent",
            "lex:PutSlotType",
            "lex:StartMigration",
        ]
        for action in actions:
            self.assertTrue(action in results)

    def test_services_with_multiple_pages_kinesis_analytics(self):
        """Ensure that Kinesis Analytics V1 actions are both present in the ses namespace"""
        # Kinesis Analytics V1
        results = get_actions_for_service("kinesisanalytics")
        actions = [
            "kinesisanalytics:GetApplicationState",  # Only in v1, not v2
            "kinesisanalytics:ListApplications",  # In both
        ]
        for action in actions:
            self.assertTrue(action in results)

    def test_services_with_multiple_pages_ses(self):
        """Ensure that ses v1 and ses v2 actions are both present in the ses namespace"""
        # SES V1: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonses.html
        self.assertTrue("ses:PutIdentityPolicy" in self.all_actions)
        # SES V2: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonsimpleemailservicev2.html
        self.assertTrue("ses:ListImportJobs" in self.all_actions)

        results = get_actions_for_service("ses")
        actions = [
            "ses:CloneReceiptRuleSet",
            "ses:CreateConfigurationSetTrackingOptions",
            "ses:CreateReceiptFilter",
            "ses:CreateReceiptRule",
            "ses:CreateReceiptRuleSet",
            "ses:CreateTemplate",
            "ses:DeleteConfigurationSetTrackingOptions",
            "ses:DeleteIdentity",
            "ses:DeleteIdentityPolicy",
            "ses:DeleteReceiptFilter",
            "ses:DeleteReceiptRule",
            "ses:DeleteReceiptRuleSet",
            "ses:DeleteTemplate",
            "ses:DeleteVerifiedEmailAddress",
            "ses:DescribeActiveReceiptRuleSet",
            "ses:DescribeConfigurationSet",
            "ses:DescribeReceiptRule",
            "ses:DescribeReceiptRuleSet",
            "ses:GetAccountSendingEnabled",
            "ses:GetIdentityDkimAttributes",
            "ses:GetIdentityMailFromDomainAttributes",
            "ses:GetIdentityNotificationAttributes",
            "ses:GetIdentityPolicies",
            "ses:GetIdentityVerificationAttributes",
            "ses:GetSendQuota",
            "ses:GetSendStatistics",
            "ses:GetTemplate",
            "ses:ListIdentities",
            "ses:ListIdentityPolicies",
            "ses:ListReceiptFilters",
            "ses:ListReceiptRuleSets",
            "ses:ListTemplates",
            "ses:ListVerifiedEmailAddresses",
            "ses:PutIdentityPolicy",
            "ses:ReorderReceiptRuleSet",
            "ses:SendBounce",
            "ses:SendBulkTemplatedEmail",
            "ses:SendRawEmail",
            "ses:SendTemplatedEmail",
            "ses:SetActiveReceiptRuleSet",
            "ses:SetIdentityDkimEnabled",
            "ses:SetIdentityFeedbackForwardingEnabled",
            "ses:SetIdentityHeadersInNotificationsEnabled",
            "ses:SetIdentityMailFromDomain",
            "ses:SetIdentityNotificationTopic",
            "ses:SetReceiptRulePosition",
            "ses:TestRenderTemplate",
            "ses:UpdateAccountSendingEnabled",
            "ses:UpdateConfigurationSetReputationMetricsEnabled",
            "ses:UpdateConfigurationSetSendingEnabled",
            "ses:UpdateConfigurationSetTrackingOptions",
            "ses:UpdateReceiptRule",
            "ses:UpdateTemplate",
            "ses:VerifyDomainDkim",
            "ses:VerifyDomainIdentity",
            "ses:VerifyEmailAddress",
            "ses:VerifyEmailIdentity",
        ]
        for action in actions:
            self.assertTrue(action in results)


class IAMDefinitionQAForServicesWithChangedHTMLFiles(unittest.TestCase):
    def setUp(self) -> None:
        all_actions = get_all_actions()
        self.all_actions = list(all_actions)
        self.all_actions.sort()

    def test_other_iam_data_fixes_in_GH_393(self):
        """Other missing actions from GH #393"""
        # Cassandra: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonkeyspacesforapachecassandra.html
        results = get_actions_for_service("cassandra")
        self.assertTrue("cassandra:Restore" in results)
        # Comprehend Medical: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazoncomprehendmedical.html
        results = get_actions_for_service("comprehendmedical")
        # print(results)
        actions = [
            "comprehendmedical:DescribeEntitiesDetectionV2Job",
            "comprehendmedical:DescribeICD10CMInferenceJob",
            "comprehendmedical:DescribePHIDetectionJob",
            "comprehendmedical:DescribeRxNormInferenceJob",
            # "comprehendmedical:DescribeSNOMEDCTInferenceJob",  # Not in SAR
            "comprehendmedical:DetectEntitiesV2",
            "comprehendmedical:InferICD10CM",
            "comprehendmedical:InferRxNorm",
            # "comprehendmedical:InferSNOMEDCT",  # Not in SAR
            "comprehendmedical:ListEntitiesDetectionV2Jobs",
            "comprehendmedical:ListICD10CMInferenceJobs",
            "comprehendmedical:ListPHIDetectionJobs",
            "comprehendmedical:ListRxNormInferenceJobs",
            # "comprehendmedical:ListSNOMEDCTInferenceJobs",  # Not in SAR
            "comprehendmedical:StartEntitiesDetectionV2Job",
            "comprehendmedical:StartICD10CMInferenceJob",
            "comprehendmedical:StartPHIDetectionJob",
            "comprehendmedical:StartRxNormInferenceJob",
            "comprehendmedical:StopEntitiesDetectionV2Job",
            "comprehendmedical:StopICD10CMInferenceJob",
        ]
        for action in actions:
            # if action not in results:
            #     print(action)
            self.assertTrue(action in results)
        # Compute Optimizer
        results = get_actions_for_service("compute-optimizer")
        actions = [
            "compute-optimizer:DeleteRecommendationPreferences",
            "compute-optimizer:ExportEBSVolumeRecommendations",
            "compute-optimizer:ExportLambdaFunctionRecommendations",
            "compute-optimizer:GetEffectiveRecommendationPreferences",
            "compute-optimizer:GetEnrollmentStatusesForOrganization",
            "compute-optimizer:GetLambdaFunctionRecommendations",
            "compute-optimizer:GetRecommendationPreferences",
            "compute-optimizer:PutRecommendationPreferences",
        ]
        for action in actions:
            self.assertTrue(action in results)
        # DataSync
        results = get_actions_for_service("datasync")
        actions = [
            "datasync:UpdateLocationNfs",
            "datasync:UpdateLocationObjectStorage",
            "datasync:UpdateLocationSmb",
            "datasync:UpdateTaskExecution",
        ]
        for action in actions:
            self.assertTrue(action in results)

        # Account Management
        results = get_actions_for_service("account")
        actions = [
            "account:DeleteAlternateContact",
            "account:GetAlternateContact",
            "account:PutAlternateContact",
        ]
        for action in actions:
            self.assertTrue(action in results)

        # AWS IAM Access Analyzer
        results = get_actions_for_service("access-analyzer")
        actions = [
            "access-analyzer:CancelPolicyGeneration",
            "access-analyzer:CreateAccessPreview",
            "access-analyzer:GetAccessPreview",
            "access-analyzer:GetGeneratedPolicy",
            "access-analyzer:ListAccessPreviewFindings",
            "access-analyzer:ListAccessPreviews",
            "access-analyzer:ListPolicyGenerations",
            "access-analyzer:StartPolicyGeneration",
            "access-analyzer:ValidatePolicy",
        ]
        for action in actions:
            self.assertTrue(action in results)
        # Elemental Activations
        results = get_actions_for_service("elemental-activations")
        actions = [
            "elemental-activations:CompleteAccountRegistration",
            "elemental-activations:StartFileUpload",
        ]
        for action in actions:
            self.assertTrue(action in results)
        # OpenSearch
        results = get_actions_for_service("es")
        actions = [
            "es:DescribeDomainChangeProgress",
        ]
        for action in actions:
            self.assertTrue(action in results)
        # Location
        results = get_actions_for_service("geo")
        actions = [
            "geo:CalculateRouteMatrix",
        ]
        for action in actions:
            self.assertTrue(action in results)

        # Amazon Managed Grafana
        results = get_actions_for_service("grafana")
        actions = [
            "grafana:DescribeWorkspaceAuthentication",
            "grafana:UpdateWorkspaceAuthentication",
        ]
        for action in actions:
            self.assertTrue(action in results)

        # EC2 Image Builder
        results = get_actions_for_service("imagebuilder")
        actions = [
            "imagebuilder:ImportVmImage",
        ]
        for action in actions:
            self.assertTrue(action in results)
        # Timestream
        results = get_actions_for_service("timestream")
        actions = [
            "timestream:CreateScheduledQuery",
            "timestream:DeleteScheduledQuery",
            "timestream:DescribeScheduledQuery",
            "timestream:ExecuteScheduledQuery",
            "timestream:ListScheduledQueries",
            "timestream:UpdateScheduledQuery",
        ]
        for action in actions:
            self.assertTrue(action in results)

        # AWS Transfer Family
        results = get_actions_for_service("transfer")
        actions = [
            "transfer:CreateAccess",
            "transfer:CreateWorkflow",
            "transfer:DeleteAccess",
            "transfer:DeleteWorkflow",
            "transfer:DescribeAccess",
            "transfer:DescribeExecution",
            "transfer:DescribeWorkflow",
            "transfer:ListAccesses",
            "transfer:ListExecutions",
            "transfer:ListWorkflows",
            "transfer:SendWorkflowStepState",
            "transfer:UpdateAccess",
        ]
        for action in actions:
            self.assertTrue(action in results)

    def test_kafka_action_names_overlap_issue(self):
        """Ensure that kafka actions are not overwritten in the IAM definition"""
        # Kafka actions used to be in two pages but are now one. This verifies the current state.
        # results = get_actions_for_service("kafka")
        # print(results)
        actions = [
            "kafka:BatchAssociateScramSecret",
            "kafka:BatchDisassociateScramSecret",
            "kafka:CreateClusterV2",
            "kafka:DeleteConfiguration",
            "kafka:DescribeClusterV2",
            "kafka:ListClustersV2",
            "kafka:ListConfigurationRevisions",
            "kafka:ListKafkaVersions",
            "kafka:ListScramSecrets",
            "kafka:RebootBroker",
            "kafka:UpdateBrokerType",
            "kafka:UpdateConfiguration",
            "kafka:UpdateConnectivity",
            "kafka:UpdateSecurity",
        ]

        for action in actions:
            self.assertTrue(action in self.all_actions)
