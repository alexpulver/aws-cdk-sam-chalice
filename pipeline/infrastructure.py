from aws_cdk import (
    core as cdk,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines
)

from api.infrastructure import Api
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class DeploymentUnit(cdk.Stage):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        database_stack = cdk.Stack(self, 'DatabaseStack')
        database = Database(database_stack, 'Database')

        api_stack = cdk.Stack(self, 'ApiStack')
        api = Api(api_stack, 'Api', database)

        monitoring_stack = cdk.Stack(self, 'MonitoringStack')
        Monitoring(monitoring_stack, 'Monitoring', database, api)


class AwsCdkSamChalicePipeline(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        cloud_assembly_artifact = codepipeline.Artifact()
        source_artifact = codepipeline.Artifact()
        source_action = codepipeline_actions.GitHubSourceAction(
            action_name='GitHub', output=source_artifact,
            oauth_token=cdk.SecretValue.secrets_manager('GITHUB_TOKEN_NAME'),
            owner='OWNER', repo='REPO', branch='main')
        synth_action = pipelines.SimpleSynthAction.standard_npm_synth(
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact)

        pipeline = pipelines.CdkPipeline(
            self, 'CdkPipeline', cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=source_action, synth_action=synth_action)
        deployment_unit = DeploymentUnit(self, 'Test')
        pipeline.add_application_stage(deployment_unit)
