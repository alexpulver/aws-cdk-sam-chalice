from aws_cdk import core as cdk

from dev import AwsCdkSamChaliceDev
from pipeline.infrastructure import AwsCdkSamChalicePipeline

app = cdk.App()

pipeline_env = cdk.Environment(account='123456789012', region='eu-west-1')

AwsCdkSamChaliceDev(app, 'AwsCdkSamChaliceDev')
AwsCdkSamChalicePipeline(app, 'AwsCdkSamChalicePipeline', env=pipeline_env)

app.synth()
