CDK_APP_NAME = "UserManagementBackend"

# pylint: disable=line-too-long
GITHUB_CONNECTION_ARN = "arn:aws:codestar-connections:eu-west-1:807650736403:connection/1f244295-871f-411f-afb1-e6ca987858b6"
GITHUB_OWNER = "alexpulver"
GITHUB_REPO = "aws-cdk-sam-chalice"
GITHUB_TRUNK_BRANCH = "future"

PIPELINE_ACCOUNT = "807650736403"
PIPELINE_REGION = "eu-west-1"
CONTINUOUS_BUILD_ACCOUNT = "807650736403"
CONTINUOUS_BUILD_REGION = "eu-west-1"
PROD_ACCOUNT = "807650736403"
PROD_REGION = "eu-west-1"

CODEBUILD_INSTALL_COMMANDS = ["./scripts/install-deps.sh"]
CODEBUILD_INSTALL_RUNTIME_VERSIONS = {"python": "3.7"}
CODEBUILD_BUILD_COMMANDS = ["./scripts/run-tests.sh", "npx cdk synth"]
