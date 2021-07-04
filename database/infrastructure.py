from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk


class Database(cdk.Construct):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(
        self,
        scope: cdk.Construct,
        id: str,
        *,
        dynamodb_billing_mode: dynamodb.BillingMode
    ) -> None:
        super().__init__(scope, id)

        partition_key = dynamodb.Attribute(
            name="username", type=dynamodb.AttributeType.STRING
        )
        self.table = dynamodb.Table(
            self,
            "Table",
            billing_mode=dynamodb_billing_mode,
            partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
