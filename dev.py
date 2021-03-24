import os

from aws_cdk import core as cdk

from api.infrastructure import Api


class Dev(cdk.Stack):

    env = cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION'])

    def __init__(self, scope, id):
        super().__init__(scope, id, env=Dev.env)
        storage = Storage(self, 'Storage')
        api = Api(self, 'Api', storage)
        monitoring = Monitoring(self, 'Monitoring', storage, api)

