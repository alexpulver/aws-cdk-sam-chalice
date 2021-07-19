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

        stateful = Stateful(
            self,
            "Stateful",
            database_dynamodb_billing_mode=database_dynamodb_billing_mode,
        )
        stateless = Stateless(
            self,
            "Stateless",
            database=stateful.database,
            api_lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )
        self.api_endpoint_url = stateless.api_endpoint_url


class Stateful(cdk.Stack):
    def __init__(
        self,
        scope: cdk.Construct,
        id_: str,
        *,
        database_dynamodb_billing_mode: dynamodb.BillingMode,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        self.database = Database(
            self, "Database", dynamodb_billing_mode=database_dynamodb_billing_mode
        )


class Stateless(cdk.Stack):
    def __init__(
        self,
        scope: cdk.Construct,
        id_: str,
        *,
        database: Database,
        api_lambda_reserved_concurrency: int,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        api = API(
            self,
            "API",
            dynamodb_table=database.table,
            lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )
        Monitoring(self, "Monitoring", database=database, api=api)

        self.api_endpoint_url = api.endpoint_url
