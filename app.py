import os

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

import constants
from deployment import UserManagementBackend
from pipeline import Pipeline

app = cdk.App()

# Development
UserManagementBackend(
    app,
    f"{constants.CDK_APP_NAME}-Dev",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    database_dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
)

# Production pipeline
Pipeline(
    app,
    f"{constants.CDK_APP_NAME}-Pipeline",
    env=cdk.Environment(
        account=constants.PIPELINE_ACCOUNT, region=constants.PIPELINE_REGION
    ),
)

app.synth()
