import os

from aws_cdk import core as cdk

from stacks.web_api import WebApi


app = cdk.App()

dev_env = cdk.Environment(
    account=os.environ['CDK_DEFAULT_ACCOUNT'],
    region=os.environ['CDK_DEFAULT_REGION'])
prod_eu_west_1_env = cdk.Environment(account='123456789012', region='eu-west-1')
prod_us_east_1_env = cdk.Environment(account='123456789012', region='us-east-1')

WebApi(app, 'WebApiDev', env=dev_env)
WebApi(app, 'WebApiProdEuWest1', env=prod_eu_west_1_env)
WebApi(app, 'WebApiProdUsEast1', env=prod_us_east_1_env)

app.synth()
