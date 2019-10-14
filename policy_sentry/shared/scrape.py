#!/usr/bin/env python3
import yaml
import os
missing_dependencies = []
try:
    import pandas as pd
except ImportError:
    missing_dependencies.append('pandas')

irregular_service_names = {  # TODO set this as a constant in a header file
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
    'elastic-inference': 'elasticinference',
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
irregular_service_links = {  # TODO set this as a constant in a header file
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
    'dbqms': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_databasequerymetadataservice.html'
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
    'iq-permissions': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsiqpermissions.html',
    ],
    'neptune-db': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonneptune.html'
    ],
    'rds-data': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonrdsdataapi.html'
    ],
    'servicequotas': [
        'https://docs.aws.amazon.com/IAM/latest/UserGuide/list_servicequotas.html'
    ],
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


def get_html(directory, requested_service):
    links = []
    links_yml_file = os.path.abspath(os.path.dirname(__file__)) + '/links.yml'
    with open(links_yml_file, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    for service_name in cfg:
        if service_name == requested_service:
            links.extend(cfg[service_name])
    html_list = []
    for link in links:
        try:
            parsed_html = pd.read_html(directory + '/' + link)
            html_list.append(parsed_html)
        except ValueError as e:
            if 'No tables found' in str(e):
                pass
            else:
                raise e

    return html_list
