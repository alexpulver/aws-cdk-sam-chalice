from aws_cdk import (
    core as cdk,
    pipelines
)

from api.infrastructure import Api
from database import Database
from monitoring import Monitoring


class DeploymentUnit(cdk.Stage):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(self, scope, id, **kwargs)

        database_stack = cdk.Stack(self, 'DatabaseStack')
        database = Database(database_stack, 'Database')

        api_stack = cdk.Stack(self, 'ApiStack')
        api = Api(api_stack, 'Api', database)

        monitoring_stack = cdk.Stack(self, 'MonitoringStack')
        Monitoring(monitoring_stack, 'Monitoring', database, api)


class Pipeline(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(self, scope, id, **kwargs)

        pipeline = pipelines.CdkPipeline(self, 'CdkPipeline')
        deployment_unit = DeploymentUnit(self, 'DeploymentUnit')
        pipeline.add_application_stage(deployment_unit)
