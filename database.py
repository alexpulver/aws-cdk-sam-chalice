from aws_cdk import (
    aws_dynamodb as dynamodb,
    core as cdk
)


class Database(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        partition_key = dynamodb.Attribute(
            name='username', type=dynamodb.AttributeType.STRING)
        self.dynamodb_table = dynamodb.Table(
            self, 'UsersTable', partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY)
        cdk.CfnOutput(self, 'UsersTableName', value=self.dynamodb_table.table_name)
