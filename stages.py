from aws_cdk import core as cdk

from api.infrastructure import Api
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class Deployment(cdk.Stage):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        application = cdk.Stack(self, 'Application')
        database = Database(application, 'Database')
        api = Api(application, 'Api', database)
        Monitoring(application, 'Monitoring', database, api)
