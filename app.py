import os

from aws_cdk import core as cdk

from config import APPLICATION_NAME
from pipeline.infrastructure import Pipeline
from stacks import Deployment

app = cdk.App()

dev_env = cdk.Environment(account=os.environ['CDK_DEFAULT_ACCOUNT'], region=os.environ['CDK_DEFAULT_REGION'])
pipeline_env = cdk.Environment(account='807650736403', region='eu-west-1')

Deployment(app, f'{APPLICATION_NAME}-Dev', env=dev_env)
Pipeline(app, f'{APPLICATION_NAME}-Pipeline', env=pipeline_env)

app.synth()
