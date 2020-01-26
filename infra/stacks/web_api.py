import os

from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    core as cdk
)
from cdk_chalice import Chalice


class WebApi(cdk.Stack):

    _API_HANDLER_LAMBDA_MEMORY_SIZE = 128
    _API_HANDLER_LAMBDA_TIMEOUT = 10

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        partition_key = dynamodb.Attribute(name='username',
                                           type=dynamodb.AttributeType.STRING)
        self.dynamodb_table = dynamodb.Table(
            self, 'UsersTable', partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY)
        cdk.CfnOutput(self, 'UsersTableName', value=self.dynamodb_table.table_name)

        lambda_service_principal = iam.ServicePrincipal('lambda.amazonaws.com')
        cloudwatch_logs_policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            'service-role/AWSLambdaBasicExecutionRole')
        self.api_handler_iam_role = iam.Role(
            self, 'ApiHandlerLambdaRole', assumed_by=lambda_service_principal,
            managed_policies=[cloudwatch_logs_policy])

        self.dynamodb_table.grant_read_write_data(self.api_handler_iam_role)

        web_api_source_dir = os.path.join(os.path.dirname(__file__), os.pardir,
                                          os.pardir, 'web-api')
        chalice_stage_config = self._create_chalice_stage_config()
        self.chalice = Chalice(self, 'WebApi', source_dir=web_api_source_dir,
                               stage_config=chalice_stage_config)

    def _create_chalice_stage_config(self):
        chalice_stage_config = {
            'api_gateway_stage': 'v1',
            'lambda_functions': {
                'api_handler': {
                    'manage_iam_role': False,
                    'iam_role_arn': self.api_handler_iam_role.role_arn,
                    'environment_variables': {
                        'DYNAMODB_TABLE_NAME': self.dynamodb_table.table_name
                    },
                    'lambda_memory_size': WebApi._API_HANDLER_LAMBDA_MEMORY_SIZE,
                    'lambda_timeout': WebApi._API_HANDLER_LAMBDA_TIMEOUT
                }
            }
        }

        return chalice_stage_config
