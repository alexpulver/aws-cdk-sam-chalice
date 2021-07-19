from typing import Any

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from api.infrastructure import API
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class UserManagementBackend(cdk.Stage):
    def __init__(
        self,
        scope: cdk.Construct,
        id_: str,
        *,
        database_dynamodb_billing_mode: dynamodb.BillingMode,
        api_lambda_reserved_concurrency: int,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        stateful = cdk.Stack(self, "Stateful")
        database = Database(
            stateful, "Database", dynamodb_billing_mode=database_dynamodb_billing_mode
        )
        stateless = cdk.Stack(self, "Stateless")
        api = API(
            stateless,
            "API",
            dynamodb_table=database.table,
            lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )
        Monitoring(stateless, "Monitoring", database=database, api=api)

        self.api_endpoint_url = api.endpoint_url
