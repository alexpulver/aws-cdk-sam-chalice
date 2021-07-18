from typing import Any

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from api.infrastructure import API
from database.infrastructure import Database
from monitoring.infrastructure import Monitoring


class Stateful(cdk.Stack):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(
        self,
        scope: cdk.Construct,
        id: str,
        *,
        dynamodb_billing_mode: dynamodb.BillingMode,
        **kwargs: Any,
    ):
        super().__init__(scope, id, **kwargs)

        self.database = Database(
            self, "Database", dynamodb_billing_mode=dynamodb_billing_mode
        )


class Stateless(cdk.Stack):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(
        self,
        scope: cdk.Construct,
        id: str,
        *,
        database: Database,
        api_lambda_reserved_concurrency: int,
        **kwargs: Any,
    ):
        super().__init__(scope, id, **kwargs)

        api = API(
            self,
            "API",
            dynamodb_table=database.table,
            lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )
        Monitoring(self, "Monitoring", database=database, api=api)

        self.api_endpoint_url = api.endpoint_url
