import json
import pathlib
from typing import Any

from aws_cdk import aws_codebuild as codebuild
from aws_cdk import core as cdk
from aws_cdk import pipelines

import constants
from deployment import ContinuousBuild
from deployment import UserManagementBackend


class Pipeline(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        codepipeline_source = pipelines.CodePipelineSource.connection(
            f"{constants.GITHUB_OWNER}/{constants.GITHUB_REPO}",
            constants.GITHUB_TRUNK_BRANCH,
            connection_arn=constants.GITHUB_CONNECTION_ARN,
        )
        synth_python_version = {
            "phases": {
                "install": {
                    "runtime-versions": constants.CODEBUILD_INSTALL_RUNTIME_VERSIONS
                }
            }
        }
        synth_codebuild_step = pipelines.CodeBuildStep(
            "Synth",
            input=codepipeline_source,
            partial_build_spec=codebuild.BuildSpec.from_object(synth_python_version),
            install_commands=constants.CODEBUILD_INSTALL_COMMANDS,
            commands=constants.CODEBUILD_BUILD_COMMANDS,
            primary_output_directory="cdk.out",
        )
        codepipeline = pipelines.CodePipeline(
            self,
            "CodePipeline",
            cli_version=Pipeline._get_cdk_cli_version(),
            synth=synth_codebuild_step,
        )

        self._add_continuous_build_stage(codepipeline)
        self._add_prod_stage(codepipeline)

    @staticmethod
    def _get_cdk_cli_version() -> str:
        package_json_path = (
            pathlib.Path(__file__).resolve().parent.joinpath("package.json")
        )
        with open(package_json_path) as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = str(package_json["devDependencies"]["aws-cdk"])
        return cdk_cli_version

    def _add_continuous_build_stage(self, codepipeline: pipelines.CodePipeline) -> None:
        continuous_build_stage = ContinuousBuild(
            self,
            f"{constants.CDK_APP_NAME}-ContinuousBuild",
            env=constants.CONTINUOUS_BUILD_ENV,
        )
        codepipeline.add_stage(continuous_build_stage)

    def _add_prod_stage(self, codepipeline: pipelines.CodePipeline) -> None:
        prod_stage = UserManagementBackend(
            self,
            f"{constants.CDK_APP_NAME}-Prod",
            env=constants.PROD_ENV,
            api_lambda_reserved_concurrency=constants.PROD_API_LAMBDA_RESERVED_CONCURRENCY,
            database_dynamodb_billing_mode=constants.PROD_DATABASE_DYNAMODB_BILLING_MODE,
        )
        api_endpoint_url_env_var = f"{constants.CDK_APP_NAME.upper()}_API_ENDPOINT_URL"
        smoke_test_commands = [f"curl ${api_endpoint_url_env_var}"]
        smoke_test_shell_step = pipelines.ShellStep(
            "SmokeTest",
            env_from_cfn_outputs={
                api_endpoint_url_env_var: prod_stage.api_endpoint_url
            },
            commands=smoke_test_commands,
        )
        codepipeline.add_stage(prod_stage, post=[smoke_test_shell_step])
