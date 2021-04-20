import os

from aws_cdk import core as cdk

from api.infrastructure import Api
from database import Database
from monitoring import Monitoring


class Dev(cdk.Stack):

    env = cdk.Environment(
        account=os.environ['CDK_DEFAULT_ACCOUNT'],
        region=os.environ['CDK_DEFAULT_REGION'])

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, env=Dev.env, **kwargs)

        database = Database(self, 'Database')
        api = Api(self, 'Api', database)
        Monitoring(self, 'Monitoring', database, api)

