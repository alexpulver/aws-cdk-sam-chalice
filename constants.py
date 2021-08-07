CDK_APP_NAME = "UserManagementBackend"
CODEBUILD_INSTALL_COMMANDS = ["./scripts/install-deps.sh"]
CODEBUILD_INSTALL_RUNTIME_VERSIONS = {"python": "3.7"}
CODEBUILD_BUILD_COMMANDS = ["./scripts/run-tests.sh", "npx cdk synth"]
GITHUB_BRANCH = "future"
GITHUB_OWNER = "alexpulver"
GITHUB_REPO = "aws-cdk-sam-chalice"
