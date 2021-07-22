import json
from pathlib import Path
from typing import Any

from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk
from aws_cdk import pipelines

from deployment import UserManagementBackend


class Pipeline(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        codepipeline_source = pipelines.CodePipelineSource.connection(
            "alexpulver/aws-cdk-sam-chalice",
            "future",
            # pylint: disable=line-too-long
            connection_arn="arn:aws:codestar-connections:eu-west-1:807650736403:connection/1f244295-871f-411f-afb1-e6ca987858b6",
        )
        synth_python_version = {
            "phases": {"install": {"runtime-versions": {"python": "3.7"}}}
        }
        synth_codebuild_step = pipelines.CodeBuildStep(
            "Synth",
            input=codepipeline_source,
            partial_build_spec=codebuild.BuildSpec.from_object(synth_python_version),
            install_commands=["./scripts/install-deps.sh"],
            commands=["./scripts/run-tests.sh", "npx cdk synth"],
            primary_output_directory="cdk.out",
        )
        codepipeline = pipelines.CodePipeline(
            self,
            "CodePipeline",
            cli_version=Pipeline._get_cdk_cli_version(),
            synth=synth_codebuild_step,
        )

        self._add_prod_stage(codepipeline)

    @staticmethod
    def _get_cdk_cli_version() -> str:
        package_json_path = Path(__file__).resolve().parent.joinpath("package.json")
        with open(package_json_path) as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = str(package_json["devDependencies"]["aws-cdk"])
        return cdk_cli_version

    def _add_prod_stage(self, codepipeline: pipelines.CodePipeline) -> None:
        prod_stage = UserManagementBackend(
            self,
            f"{UserManagementBackend.__name__}-Prod",
            env=cdk.Environment(account="807650736403", region="eu-west-1"),
            api_lambda_reserved_concurrency=10,
            database_dynamodb_billing_mode=dynamodb.BillingMode.PROVISIONED,
        )
        api_endpoint_url_env_var = (
            f"{UserManagementBackend.__name__.upper()}_API_ENDPOINT_URL"
        )
        smoke_test_commands = [f"curl ${api_endpoint_url_env_var}"]
        smoke_test_shell_step = pipelines.ShellStep(
            "SmokeTest",
            env_from_cfn_outputs={
                api_endpoint_url_env_var: prod_stage.api_endpoint_url
            },
            commands=smoke_test_commands,
        )
        codepipeline.add_stage(prod_stage, post=[smoke_test_shell_step])
