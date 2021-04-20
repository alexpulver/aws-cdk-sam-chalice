from aws_cdk import core as cdk

from dev import Dev
from pipeline import Pipeline

app = cdk.App()

pipeline_env = cdk.Environment(account='123456789012', region='eu-west-1')

Dev(app, 'Dev')
Pipeline(app, 'Pipeline', env=pipeline_env)

app.synth()
