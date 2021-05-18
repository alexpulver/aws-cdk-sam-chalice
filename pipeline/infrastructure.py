import json
from pathlib import Path

from aws_cdk import (
    core as cdk,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines
)

from config import APPLICATION_NAME
from stacks import Application


class Pipeline(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name='GitHub', output=source_artifact,
            connection_arn='arn:aws:codestar-connections:eu-west-1:807650736403:connection/1f244295-871f-411f-afb1-e6ca987858b6',
            owner='alexpulver', repo='aws-cdk-sam-chalice', branch='future')
        synth_action = pipelines.SimpleSynthAction(
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_commands=['scripts/install-deps.sh'],
            build_commands=['scripts/run-tests.sh'],
            synth_command='npx cdk synth')

        package_json_path = Path(__file__).resolve().parent.parent.joinpath('package.json')
        with open(package_json_path) as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = package_json['devDependencies']['aws-cdk']
        cdk_pipeline = pipelines.CdkPipeline(
            self, 'CdkPipeline', source_action=source_action, synth_action=synth_action,
            cdk_cli_version=cdk_cli_version, cloud_assembly_artifact=cloud_assembly_artifact)

        pre_prod_env = cdk.Environment(account='807650736403', region='eu-west-1')
        pre_prod_deployment = Deployment(self, 'Deployment', stage_name='PreProd', env=pre_prod_env)
        pre_prod_stage = cdk_pipeline.add_stage('PreProd')
        pre_prod_stage.add_application(pre_prod_deployment)


class Deployment(cdk.Stage):

    def __init__(self, scope: cdk.Construct, id: str, stage_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        Application(self, 'Application', stack_name=f'{APPLICATION_NAME}-{stage_name}')
