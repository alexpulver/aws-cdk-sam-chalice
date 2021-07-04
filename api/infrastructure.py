from pathlib import Path
from typing import Any, Dict, cast

from aws_cdk import aws_iam as iam
from aws_cdk import core as cdk
from cdk_chalice import Chalice

from database.infrastructure import Database


class Api(cdk.Construct):
    _LAMBDA_MEMORY_SIZE = 128
    _LAMBDA_TIMEOUT = 10
    _RUNTIME_DIR = Path(__file__).resolve().parent.joinpath("runtime")

    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(self, scope: cdk.Construct, id: str, database: Database) -> None:
        super().__init__(scope, id)

        service_principal = iam.ServicePrincipal("lambda.amazonaws.com")
        # The policy is needed for writing to Amazon CloudWatch Logs
        policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AWSLambdaBasicExecutionRole"
        )
        handler_role = iam.Role(
            self,
            "HandlerRole",
            assumed_by=cast(iam.IPrincipal, service_principal),
            managed_policies=[policy],
        )

        database.table.grant_read_write_data(cast(iam.IGrantable, handler_role))

        chalice_stage_config = Api._create_chalice_stage_config(handler_role, database)
        self.chalice = Chalice(
            self,
            "Chalice",
            source_dir=str(Api._RUNTIME_DIR),
            stage_config=chalice_stage_config,
        )
        rest_api = self.chalice.sam_template.get_resource("RestAPI")
        rest_api.tracing_enabled = True

    @staticmethod
    def _create_chalice_stage_config(
        handler_role: iam.Role, database: Database
    ) -> Dict[str, Any]:
        chalice_stage_config = {
            "api_gateway_stage": "v1",
            "lambda_functions": {
                "api_handler": {
                    "manage_iam_role": False,
                    "iam_role_arn": handler_role.role_arn,
                    "environment_variables": {"TABLE_NAME": database.table.table_name},
                    "lambda_memory_size": Api._LAMBDA_MEMORY_SIZE,
                    "lambda_timeout": Api._LAMBDA_TIMEOUT,
                }
            },
        }
        return chalice_stage_config
