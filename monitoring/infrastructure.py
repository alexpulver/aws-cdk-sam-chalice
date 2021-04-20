from aws_cdk import (
    core as cdk
)


class Monitoring(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str, database: cdk.Construct, api: cdk.Construct, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        database.dynamodb_table.metric_consumed_read_capacity_units()
