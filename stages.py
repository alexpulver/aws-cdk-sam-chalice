from typing import Any

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from stacks import Stateful
from stacks import Stateless


class Dev(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        stateful = Stateful(
            self, "Stateful", dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        Stateless(
            self,
            "Stateless",
            database=stateful.database,
            api_lambda_reserved_concurrency=1,
        )


class PreProd(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        stateful = Stateful(
            self, "Stateful", dynamodb_billing_mode=dynamodb.BillingMode.PROVISIONED
        )
        stateless = Stateless(
            self,
            "Stateless",
            database=stateful.database,
            api_lambda_reserved_concurrency=10,
        )
        self.api_endpoint_url = stateless.api_endpoint_url
