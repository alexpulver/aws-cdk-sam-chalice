from typing import Any

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from stacks import Stateful
from stacks import Stateless


class Dev(cdk.Stage):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(self, scope: cdk.Construct, id: str, **kwargs: Any):
        super().__init__(scope, id, **kwargs)

        stateful = Stateful(
            self, "Stateful", dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        stateless = Stateless(
            self,
            "Stateless",
            database=stateful.database,
            lambda_reserved_concurrent_executions=1,
        )
        self.api_endpoint_url = stateless.api_endpoint_url


class PreProd(cdk.Stage):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(self, scope: cdk.Construct, id: str, **kwargs: Any):
        super().__init__(scope, id, **kwargs)

        stateful = Stateful(
            self, "Stateful", dynamodb_billing_mode=dynamodb.BillingMode.PROVISIONED
        )
        stateless = Stateless(
            self,
            "Stateless",
            database=stateful.database,
            lambda_reserved_concurrent_executions=10,
        )
        self.api_endpoint_url = stateless.api_endpoint_url
