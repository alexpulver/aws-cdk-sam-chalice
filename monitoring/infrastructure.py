from typing import cast

from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import core as cdk

from api.infrastructure import API
from database.infrastructure import Database


class Monitoring(cdk.Construct):
    # pylint: disable=redefined-builtin
    # The 'id' parameter name is CDK convention.
    def __init__(
        self, scope: cdk.Construct, id: str, *, database: Database, api: API
    ) -> None:
        super().__init__(scope, id)

        apigateway = api.chalice.sam_template.get_resource("RestAPI")
        apigateway_metric_dimensions = {"ApiName": cdk.Fn.ref(apigateway.logical_id)}
        apigateway_metric_count = cloudwatch.Metric(
            namespace="AWS/APIGateway",
            metric_name="Count",
            dimensions=apigateway_metric_dimensions,
        )
        widgets = [
            cloudwatch.SingleValueWidget(
                metrics=[apigateway_metric_count]  # type: ignore
            ),
            cloudwatch.SingleValueWidget(
                metrics=[
                    cast(
                        cloudwatch.IMetric,
                        database.table.metric_consumed_read_capacity_units(),
                    )
                ]
            ),
        ]
        cloudwatch.Dashboard(self, "Dashboard", widgets=[widgets])  # type: ignore
