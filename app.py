import os

from aws_cdk import core as cdk

from config import APP_NAME
from pipeline import Pipeline
from stages import Dev

app = cdk.App()

dev_env = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]
)
Dev(app, f"{APP_NAME}-Dev", env=dev_env)

pipeline_env = cdk.Environment(account="807650736403", region="eu-west-1")
Pipeline(app, f"{APP_NAME}-Pipeline", env=pipeline_env)

app.synth()
