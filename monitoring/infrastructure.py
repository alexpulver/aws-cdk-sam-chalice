from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import core as cdk

from api.infrastructure import Api
from database.infrastructure import Database


class Monitoring(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str, database: Database, api: Api) -> None:
        super().__init__(scope, id)

        apigateway = api.chalice.sam_template.get_resource('RestAPI')
        apigateway_metric_dimensions = {'ApiName': cdk.Fn.ref(apigateway.logical_id)}
        apigateway_metric_count = cloudwatch.Metric(
            namespace='AWS/APIGateway', metric_name='Count', dimensions=apigateway_metric_dimensions)
        widgets = [
            cloudwatch.SingleValueWidget(metrics=[apigateway_metric_count]),
            cloudwatch.SingleValueWidget(metrics=[database.table.metric_consumed_read_capacity_units()])
        ]
        cloudwatch.Dashboard(self, 'Dashboard', widgets=[widgets])
