import os

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from config import APPLICATION_NAME
from deployment import Deployment
from pipeline import Pipeline

app = cdk.App()

dev_env = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]
)
pipeline_env = cdk.Environment(account="807650736403", region="eu-west-1")

Deployment(
    app,
    f"{APPLICATION_NAME}-Dev",
    dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
    env=dev_env,
)
Pipeline(app, f"{APPLICATION_NAME}-Pipeline", env=pipeline_env)

app.synth()
