import json
from pathlib import Path
from typing import Any

from aws_cdk import core as cdk
from aws_cdk import pipelines

from config import APP_NAME
from stages import PreProd


class Pipeline(cdk.Stack):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(self, scope: cdk.Construct, id: str, **kwargs: Any):
        super().__init__(scope, id, **kwargs)

        codepipeline_source = pipelines.CodePipelineSource.connection(
            "alexpulver/aws-cdk-sam-chalice",
            "future",
            # pylint: disable=line-too-long
            connection_arn="arn:aws:codestar-connections:eu-west-1:807650736403:connection/1f244295-871f-411f-afb1-e6ca987858b6",
        )
        synth_commands = [
            "pyenv local 3.7.10",
            "./scripts/install-deps.sh",
            "./scripts/run-tests.sh",
            "npx cdk synth",
        ]
        synth_shell_step = pipelines.ShellStep(
            "Synth", input=codepipeline_source, commands=synth_commands
        )
        codepipeline = pipelines.CodePipeline(
            self,
            "CodePipeline",
            cli_version=Pipeline._get_cdk_cli_version(),
            cross_account_keys=True,
            publish_assets_in_parallel=False,
            synth=synth_shell_step,
        )

        self._add_pre_prod_stage(codepipeline)

    @staticmethod
    def _get_cdk_cli_version() -> str:
        package_json_path = Path(__file__).resolve().parent.joinpath("package.json")
        with open(package_json_path) as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = str(package_json["devDependencies"]["aws-cdk"])
        return cdk_cli_version

    def _add_pre_prod_stage(self, codepipeline: pipelines.CodePipeline) -> None:
        pre_prod_env = cdk.Environment(account="807650736403", region="eu-west-1")
        pre_prod_stage = PreProd(self, f"{APP_NAME}-PreProd", env=pre_prod_env)

        api_endpoint_url_env_var = f"{APP_NAME.upper()}_API_ENDPOINT_URL"
        smoke_test_commands = [f"curl ${api_endpoint_url_env_var}"]
        smoke_test_shell_step = pipelines.ShellStep(
            "SmokeTest",
            env_from_cfn_outputs={
                api_endpoint_url_env_var: pre_prod_stage.api_endpoint_url
            },
            commands=smoke_test_commands,
        )

        codepipeline.add_stage(pre_prod_stage, post=[smoke_test_shell_step])
