from aws_cdk import (
    core as cdk,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines
)

from api.infrastructure import Api
from config import APPLICATION_NAME
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


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
            install_commands=['npm install', 'pip install -r requirements.txt'],
            synth_command='npx cdk synth')

        # TODO: Use the CDK CLI version number from package.json dynamically
        cdk_pipeline = pipelines.CdkPipeline(
            self, 'CdkPipeline', source_action=source_action, synth_action=synth_action,
            cdk_cli_version='1.103.0', cloud_assembly_artifact=cloud_assembly_artifact)

        test_env = cdk.Environment(account='807650736403', region='eu-west-1')
        test_stage = Stage(self, f'{APPLICATION_NAME}PipelineTestStage', env=test_env)
        cdk_pipeline.add_application_stage(test_stage)


class Stage(cdk.Stage):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        database_deployment_unit = cdk.Stack(self, 'DatabaseDeploymentUnit')
        database = Database(database_deployment_unit, 'Database')

        api_deployment_unit = cdk.Stack(self, 'ApiDeploymentUnit')
        api = Api(api_deployment_unit, 'Api', database)

        monitoring_deployment_unit = cdk.Stack(self, 'MonitoringDeploymentUnit')
        Monitoring(monitoring_deployment_unit, 'Monitoring', database, api)
