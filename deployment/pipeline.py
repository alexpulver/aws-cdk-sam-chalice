from aws_cdk import (
    core as cdk,
    pipelines
)


class DeploymentUnit(cdk.Stage):

    def __init__(self, scope, id, **kwargs):
        super().__init__(self, scope, id, **kwargs)

        storage = Storage(cdk.Stack(self, 'StorageStack'), 'Storage')
        api = Api(cdk.Stack(self, 'ApiStack'), 'Api', storage)
        monitoring = Monitoring(cdk.Stack(self, 'MonitoringStack'), 'Monitoring', storage, api)



class Pipeline(cdk.Stack):

    def __init__(self):
        cdk_pipeline = pipelines.CdkPipeline()

