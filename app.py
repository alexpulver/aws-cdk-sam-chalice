from aws_cdk import core as cdk

import constants
from deployment import UserManagementBackend
from pipeline import Pipeline

app = cdk.App()

# Development
UserManagementBackend(
    app,
    f"{constants.CDK_APP_NAME}-Dev",
    env=constants.DEV_ENV,
    api_lambda_reserved_concurrency=constants.DEV_API_LAMBDA_RESERVED_CONCURRENCY,
    database_dynamodb_billing_mode=constants.DEV_DATABASE_DYNAMODB_BILLING_MODE,
)

# Production pipeline
Pipeline(app, f"{constants.CDK_APP_NAME}-Pipeline", env=constants.PIPELINE_ENV)

app.synth()
