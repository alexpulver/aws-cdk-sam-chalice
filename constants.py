import os

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

CDK_APP_NAME = "UserManagementBackend"

# pylint: disable=line-too-long
GITHUB_CONNECTION_ARN = "arn:aws:codestar-connections:eu-west-1:807650736403:connection/1f244295-871f-411f-afb1-e6ca987858b6"
GITHUB_OWNER = "alexpulver"
GITHUB_REPO = "aws-cdk-sam-chalice"
GITHUB_TRUNK_BRANCH = "future"

CODEBUILD_INSTALL_COMMANDS = ["./scripts/install-deps.sh"]
CODEBUILD_INSTALL_RUNTIME_VERSIONS = {"python": "3.7"}
CODEBUILD_BUILD_COMMANDS = ["./scripts/run-tests.sh", "npx cdk synth"]

DEV_ENV = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]
)
DEV_API_LAMBDA_RESERVED_CONCURRENCY = 1
DEV_DATABASE_DYNAMODB_BILLING_MODE = dynamodb.BillingMode.PAY_PER_REQUEST

PIPELINE_ENV = cdk.Environment(account="807650736403", region="eu-west-1")

CONTINUOUS_BUILD_ENV = cdk.Environment(account="807650736403", region="eu-west-1")

PROD_ENV = cdk.Environment(account="807650736403", region="eu-west-1")
PROD_API_LAMBDA_RESERVED_CONCURRENCY = 10
PROD_DATABASE_DYNAMODB_BILLING_MODE = dynamodb.BillingMode.PROVISIONED
