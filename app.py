import os

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from deployment import UserManagementBackend
from pipeline import Pipeline

app = cdk.App()

dev_env = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]
)
pipeline_env = cdk.Environment(account="807650736403", region="eu-west-1")

UserManagementBackend(
    app,
    f"{UserManagementBackend.__name__}-Dev",
    dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    env=dev_env,
)
Pipeline(app, f"{UserManagementBackend.__name__}-Pipeline", env=pipeline_env)

app.synth()
