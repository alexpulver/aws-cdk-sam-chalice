from typing import Any

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from api.infrastructure import API
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class UserManagementBackend(cdk.Stage):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(
        self,
        scope: cdk.Construct,
        id: str,
        *,
        dynamodb_billing_mode: dynamodb.BillingMode,
        **kwargs: Any
    ):
        super().__init__(scope, id, **kwargs)

        stateful = cdk.Stack(self, "Stateful")
        database = Database(
            stateful, "Database", dynamodb_billing_mode=dynamodb_billing_mode
        )

        stateless = cdk.Stack(self, "Stateless")
        api = API(stateless, "API", database=database)
        Monitoring(stateless, "Monitoring", database=database, api=api)

        self.api_endpoint_url = api.endpoint_url
