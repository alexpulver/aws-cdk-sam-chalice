import json
from pathlib import Path
from typing import Any

from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk
from aws_cdk import pipelines

from deployment import UserManagementBackend


class Pipeline(cdk.Stack):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(self, scope: cdk.Construct, id: str, **kwargs: Any):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub",
            output=source_artifact,
            # pylint: disable=line-too-long
            connection_arn="arn:aws:codestar-connections:eu-west-1:807650736403:connection/1f244295-871f-411f-afb1-e6ca987858b6",
            owner="alexpulver",
            repo="aws-cdk-sam-chalice",
            branch="future",
        )

        synth_action = pipelines.SimpleSynthAction(
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_commands=[
                "pyenv local 3.7.10",
                "./scripts/install-deps.sh",
            ],
            test_commands=["./scripts/run-tests.sh"],
            synth_command="npx cdk synth",
        )

        cdk_pipeline = pipelines.CdkPipeline(
            self,
            "CdkPipeline",
            source_action=source_action,
            synth_action=synth_action,
            single_publisher_per_type=True,
            cdk_cli_version=Pipeline._get_cdk_cli_version(),
            cloud_assembly_artifact=cloud_assembly_artifact,
        )

        self._add_pre_prod_stage(cdk_pipeline)

    @staticmethod
    def _get_cdk_cli_version() -> str:
        package_json_path = Path(__file__).resolve().parent.joinpath("package.json")
        with open(package_json_path) as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = str(package_json["devDependencies"]["aws-cdk"])
        return cdk_cli_version

    def _add_pre_prod_stage(self, cdk_pipeline: pipelines.CdkPipeline) -> None:
        pre_prod_env = cdk.Environment(account="807650736403", region="eu-west-1")
        pre_prod_application_stage = UserManagementBackend(
            self,
            f"{UserManagementBackend.__name__}-PreProd",
            dynamodb_billing_mode=dynamodb.BillingMode.PROVISIONED,
            env=pre_prod_env,
        )

        api_endpoint_url_env_var = (
            f"{UserManagementBackend.__name__.upper()}_API_ENDPOINT_URL"
        )
        pre_prod_smoke_test_outputs = {
            api_endpoint_url_env_var: cdk_pipeline.stack_output(
                pre_prod_application_stage.api_endpoint_url
            )
        }
        pre_prod_smoke_test_commands = [f"curl ${api_endpoint_url_env_var}"]
        pre_prod_smoke_test_action = pipelines.ShellScriptAction(
            action_name="SmokeTest",
            use_outputs=pre_prod_smoke_test_outputs,
            commands=pre_prod_smoke_test_commands,
        )

        pre_prod_stage = cdk_pipeline.add_application_stage(pre_prod_application_stage)
        pre_prod_stage.add_actions(pre_prod_smoke_test_action)
