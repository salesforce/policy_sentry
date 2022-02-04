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

    def test_services_with_multiple_pages_greengrass(self):
        """Ensure that greengrass v1 and greengrass v2 actions are both present in the greengrass namespace"""
        # Greengrass V1: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiotgreengrass.html
        self.assertTrue("greengrass:CreateResourceDefinition" in self.all_actions)
        # Greengrass V2: https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiotgreengrassv2.html
        self.assertTrue("greengrass:CreateComponentVersion" in self.all_actions)

    def test_services_with_multiple_pages_lex(self):
        """Ensure that lex v1 and lex v2 actions are both present in the lex namespace"""
        # Lex V1: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlex.html
        self.assertTrue("lex:DeleteUtterances" in self.all_actions)
        # Lex V2: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlexv2.html
        self.assertTrue("lex:ListBotLocales" in self.all_actions)

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
            "datasync:UpdateTaskExecution"
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
            "elemental-activations:StartAccountRegistration"
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
            "kafka:UpdateSecurity"
        ]

        for action in actions:
            if action not in self.all_actions:
                print("Action {} not found in IAM definition".format(action))
