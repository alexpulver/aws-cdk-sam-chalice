import os

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from build import Build
from deployment import UserManagementBackend
from pipeline import Pipeline

app = cdk.App()

# Development
UserManagementBackend(
    app,
    f"{UserManagementBackend.__name__}-Dev",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    database_dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
)

# Feature branch build
Build(
    app,
    f"{UserManagementBackend.__name__}-Build",
    env=cdk.Environment(account="807650736403", region="eu-west-1"),
)

# Production pipeline
Pipeline(
    app,
    f"{UserManagementBackend.__name__}-Pipeline",
    env=cdk.Environment(account="807650736403", region="eu-west-1"),
)

app.synth()
