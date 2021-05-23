from aws_cdk import core as cdk

from api.infrastructure import Api
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class Deployment(cdk.Stage):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        Application(self, 'Application')


class Application(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        database = Database(self, 'Database')
        api = Api(self, 'Api', database)
        Monitoring(self, 'Monitoring', database, api)
