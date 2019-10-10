#!/usr/bin/env python3
import requests
from urllib.request import urlopen
import os
import yaml

missing_dependencies = []
try:
    import pandas as pd
except ImportError:
    missing_dependencies.append('pandas')

ALL_AWS_SERVICES = [
    "a4b",
    "account",
    "acm",
    "acm-pca",
    "amplify",
    "apigateway",
    "application-autoscaling",
    "appstream",
    "appsync",
    "artifact",
    "athena",
    "autoscaling",
    "autoscaling-plans",
    "aws-marketplace",
    "aws-marketplace-management",
    "aws-portal",
    "backup",
    "batch",
    "budgets",
    "ce",
    "chime",
    "cloud9",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudsearch",
    "cloudtrail",
    "cloudwatch",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codepipeline",
    "codestar",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "config",
    "connect",
    "cur",
    "datapipeline",
    "datasync",
    "dax",
    "deeplens",
    "devicefarm",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "ds",
    "dynamodb",
    "ec2",
    "ec2messages",
    "ecr",
    "ecs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elasticfilesystem",
    "elasticloadbalancing",
    "elasticmapreduce",
    "elastictranscoder",
    "es",
    "events",
    "execute-api",
    "firehose",
    "fms",
    "freertos",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "greengrass",
    "groundtruthlabeling",
    "guardduty",
    "health",
    "iam",
    "importexport",
    "inspector",
    "iot",
    "iot1click",
    "iotanalytics",
    "iotevents",
    "iotsitewise",
    "kafka",
    "kinesis",
    "kinesisanalytics",
    "kinesisvideo",
    "kms",
    "lambda",
    "lex",
    "license-manager",
    "lightsail",
    "logs",
    "machinelearning",
    "macie",
    "mechanicalturk",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediastore",
    "mediatailor",
    "mgh",
    "mobileanalytics",
    "mobilehub",
    "mobiletargeting",
    "mq",
    "neptune-db",
    "opsworks",
    "opsworks-cm",
    "organizations",
    "pi",
    "polly",
    "pricing",
    "quicksight",
    "ram",
    "rds",
    "redshift",
    "rekognition",
    "resource-groups",
    "robomaker",
    "route53",
    "route53domains",
    "route53resolver",
    "s3",
    "sagemaker",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "servicecatalog",
    "servicediscovery",
    "servicequotas",
    "ses",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssmmessages",
    "sso",
    "sso-directory",
    "states",
    "storagegateway",
    "sts",
    "sumerian",
    "support",
    "swf",
    "tag",
    "textract",
    "transcribe",
    "transfer",
    "translate",
    "trustedadvisor",
    "waf",
    "waf-regional",
    "wam",
    "wellarchitected",
    "workdocs",
    "worklink",
    "workmail",
    "workspaces",
    "xray"
]
irregular_service_names = {
    'a4b': 'alexaforbusiness',
    'appstream': 'appstream2.0',
    'acm': 'certificatemanager',
    'acm-pca': 'certificatemanagerprivatecertificateauthority',
    'aws-marketplace-management': 'marketplacemanagementportal',
    'aws-portal': 'billing',
    'budgets': 'budgetservice',
    'ce': 'costexplorerservice',
    'cognito-identity': 'cognitoidentity',
    'cognito-sync': 'cognitosync',
    'cognito-idp': 'cognitouserpools',
    'cur': 'costandusagereport',
    'dax': 'dynamodbacceleratordax',
    'dlm': 'datalifecyclemanager',
    'dms': 'databasemigrationservice',
    'ds': 'directoryservice',
    'ec2messages': 'messagedeliveryservice',
    'ecr': 'elasticcontainerregistry',
    'ecs': 'elasticcontainerservice',
    'eks': 'elasticcontainerserviceforkubernetes',
    'efs': 'elasticfilesystem',
    'es': 'elasticsearchservice',
    'events': 'cloudwatchevents',
    'firehose': 'kinesisfirehose',
    'fms': 'firewallmanager',
    # 'globalaccelerator': 'globalaccelerator',
    'greengrass': 'iotgreengrass',
    'health': 'healthapisandnotifications',
    'importexport': 'importexportdiskservice',
    'iot1click': 'iot1-click',
    'kafka': 'managedstreamingforkafka',
    'kinesisvideo': 'kinesisvideostreams',
    'kms': 'keymanagementservice',
    'license-manager': 'licensemanager',
    'logs': 'cloudwatchlogs',
    'opsworks-cm': 'opsworksconfigurationmanagement',
    'mediaconnect': 'elementalmediaconnect',
    'mediaconvert': 'elementalmediaconvert',
    'medialive': 'elementalmedialive',
    'mediapackage': 'elementalmediapackage',
    'mediastore': 'elementalmediastore',
    'mediatailor': 'elementalmediatailor',
    'mgh': 'migrationhub',
    'mobiletargeting': 'pinpoint',
    'pi': 'performanceinsights',
    'pricing': 'pricelist',
    'ram': 'resourceaccessmanager',
    'resource-groups': 'resourcegroups',
    'sdb': 'simpledb',
    'servicediscovery': 'cloudmap',
    'serverlessrepo': 'serverlessapplicationrepository',
    'sms': 'servermigrationservice',
    'sms-voice': 'pinpointsmsandvoiceservice',
    'sso-directory': 'ssodirectory',
    'ssm': 'systemsmanager',
    'ssmmessages': 'sessionmanagermessagegatewayservice',
    'states': 'stepfunctions',
    'sts': 'securitytokenservice',
    'swf': 'simpleworkflowservice',
    'tag': 'resourcegrouptaggingapi',
    'transfer': 'transferforsftp',
    'waf-regional': 'wafregional',
    'wam': 'workspacesapplicationmanager',
    'wellarchitected': 'well-architectedtool',
    'xray': 'x-ray'
}

irregular_service_links = {
    'a4b': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_alexaforbusiness.html'
    ],
    'account': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsaccounts.html'
    ],
    'apigateway': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_manageamazonapigateway.html'
    ],
    'application-autoscaling': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_applicationautoscaling.html'
    ],
    'autoscaling-plans': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsautoscaling.html'
    ],
    'aws-marketplace': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsmarketplace.html',
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsmarketplacemeteringservice.html',
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsprivatemarketplace.html'
    ],
    'comprehendmedical': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_comprehendmedical.html'
    ],
    'datapipeline': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_datapipeline.html'
    ],
    'datasync': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_datasync.html'
    ],
    'discovery': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_applicationdiscovery.html'
    ],
    'elasticloadbalancing': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_elasticloadbalancing.html',
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_elasticloadbalancingv2.html'
    ],
    'execute-api': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonapigateway.html'
    ],
    'iam': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_identityandaccessmanagement.html'
    ],
    'neptune-db': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonneptune.html'
    ],
    'servicequotas': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_servicequotas.html'
    ]
}


def get_docs_by_prefix(prefix):
    # The links on the Actions, Resources, and Condition Keys page take two different formats, both of which are shown below
    amazon_link_form = 'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazon{0}.html'
    aws_link_form = 'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_aws{0}.html'

    if prefix in irregular_service_links:
        links = irregular_service_links[prefix]
    else:
        if prefix in irregular_service_names:
            prefix = irregular_service_names[prefix]
        links = [amazon_link_form.format(prefix), aws_link_form.format(prefix)]

    return links


def get_valid_links(links):
    valid_links = []
    valid_links_shortened = []
    for link in links:
        html = requests.get(link).content
        try:
            parsed_html = pd.read_html(html)
            valid_links.append(link)
            valid_links_shortened.append(link.replace('https://docs.aws.amazon.com/IAM/latest/UserGuide/', ''))
        except ValueError as e:
            if 'No tables found' in str(e):
                pass
            else:
                raise e

    # return html_list
    return valid_links, valid_links_shortened


def main():
    valid_links = {}
    valid_links_shortened = {}
    for service in ALL_AWS_SERVICES:
        links = get_docs_by_prefix(service)
        valid_links[service], valid_links_shortened[service] = get_valid_links(links)

    # Write a YAML file that will contain the links and their mappings to various services.
    # This should have the 'https://docs.aws.amazon.com/IAM/latest/UserGuide/' portion removed
    # that will be used by policy_sentry to read those files and build the tables
    with open('./shared/links.yml', 'w+') as outfile:
        yaml.dump(valid_links_shortened, outfile, default_flow_style=False)
    outfile.close()

    # Write a text file with the list of links.
    links_file = './utils/links.txt'
    if os.path.exists(links_file):
        os.remove(links_file)

    with open(links_file, 'w+') as fileobj:
        for service in valid_links:
            for link in valid_links[service]:
                fileobj.write(link)
                fileobj.write('\n')
                fileobj.flush()
    fileobj.close()


if __name__ == '__main__':
    main()
