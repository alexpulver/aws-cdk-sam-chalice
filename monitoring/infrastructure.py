from aws_cdk import (
    core as cdk
)

from api.infrastructure import Api
from database.infrastructure import Database


class Monitoring(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str, database: Database, api: Api, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        database.table.metric_consumed_read_capacity_units()
