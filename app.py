from aws_cdk import core as cdk

from config import APPLICATION_NAME
from dev import Dev
from pipeline.infrastructure import Pipeline

app = cdk.App()

pipeline_env = cdk.Environment(account='807650736403', region='eu-west-1')

Dev(app, f'{APPLICATION_NAME}Dev')
Pipeline(app, f'{APPLICATION_NAME}Pipeline', env=pipeline_env)

app.synth()
