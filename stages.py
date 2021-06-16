from typing import Any

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from api.infrastructure import Api
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class Deployment(cdk.Stage):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(
        self,
        scope: cdk.Construct,
        id: str,
        dynamodb_billing_mode: dynamodb.BillingMode,
        **kwargs: Any
    ):
        super().__init__(scope, id, **kwargs)

        application = cdk.Stack(self, "Application")
        database = Database(application, "Database", dynamodb_billing_mode)
        api = Api(application, "Api", database)
        Monitoring(application, "Monitoring", database, api)

        self.api_endpoint_url = api.chalice.sam_template.get_output("EndpointURL")
