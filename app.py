import os

from aws_cdk import core as cdk

from infrastructure import AwsCdkSamChalice


app = cdk.App()

dev_env = cdk.Environment(
    account=os.environ['CDK_DEFAULT_ACCOUNT'],
    region=os.environ['CDK_DEFAULT_REGION'])
prod_eu_west_1_env = cdk.Environment(account='123456789012', region='eu-west-1')
prod_us_east_1_env = cdk.Environment(account='123456789012', region='us-east-1')

AwsCdkSamChalice(app, 'AwsCdkSamChaliceDev', env=dev_env)
AwsCdkSamChalice(app, 'AwsCdkSamChaliceProdEuWest1', env=prod_eu_west_1_env)
AwsCdkSamChalice(app, 'AwsCdkSamChaliceProdUsEast1', env=prod_us_east_1_env)

app.synth()
