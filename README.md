# Example project for working with AWS CDK, AWS SAM and AWS Chalice
This project shows how AWS CDK and AWS Chalice can be used
together to deliver a service using CDK for building the broader service
infrastructure, and Chalice as developer-friendly Python serverless 
microframework.

The service being built is based on Amazon API Gateway and AWS Lambda, 
and provides basic CRUD operations for managing users in a DynamoDB table.

## Create development environment
See [Getting Started With the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
for additional details and prerequisites

### Clone the code
```bash
git clone -b future https://github.com/alexpulver/aws-cdk-sam-chalice
cd aws-cdk-sam-chalice
```

### Create Python virtual environment and install the dependencies
```bash
python3.7 -m venv .venv
source .venv/bin/activate
./scripts/install-deps.sh
./scripts/run-tests.sh
```

### [Optional] Upgrade AWS CDK Toolkit version
```bash
vi package.json  # Update "aws-cdk" package version
./scripts/install-deps.sh
```

### [Optional] Upgrade dependencies (ordered by constraints)
Consider [AWS CDK Toolkit (CLI)](https://docs.aws.amazon.com/cdk/latest/guide/reference.html#versioning) compatibility 
when choosing AWS CDK packages version.

Upgrade all top-level AWS CDK packages explicitly to keep their versions in sync.
This will not be required with AWS CDK v2. See [Migrating to AWS CDK v2](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-v2.html) 
for details.

```bash
_cdk_version=CDK_VERSION
pip install pip-tools==6.1.0
pip-compile --upgrade api/runtime/requirements.in
pip-compile \
  --upgrade requirements.in \
  --upgrade-package aws_cdk.aws_dynamodb==${_cdk_version} \
  --upgrade-package aws_cdk.pipelines==${_cdk_version} \
  --upgrade-package aws_cdk.core==${_cdk_version}
pip-compile --upgrade requirements-dev.in
./scripts/install-deps.sh
./scripts/run-tests.sh
```

## Deploy development stack
The `AwsCdkSamChalice-Dev/Application` stack uses your default account and region.

```bash
npx cdk deploy AwsCdkSamChalice-Dev/Application
```

Example output for `npx cdk deploy AwsCdkSamChalice-Dev/Application` stack:
```text
AwsCdkSamChaliceDevApplication1F0BF25A.APIHandlerArn = arn:aws:lambda:eu-west-1:123456789012:function:AwsCdkSamChalice-Dev-Application-APIHandler-1PEIOK9ZRGT4D
AwsCdkSamChaliceDevApplication1F0BF25A.APIHandlerName = AwsCdkSamChalice-Dev-Application-APIHandler-1PEIOK9ZRGT4D
AwsCdkSamChaliceDevApplication1F0BF25A.EndpointURL = https://usuf95bc7a.execute-api.eu-west-1.amazonaws.com/v1/
AwsCdkSamChaliceDevApplication1F0BF25A.RestAPIId = usuf95bc7a
```

## Deploy pipeline stack
**Prerequisites**
- Fork the repository and create AWS CodeStar Connections [connection](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html) for it
- Update `source_action` in `pipeline/infrastructure.py` with the connection, owner and repository details from previous step
- Update `pre_prod_env` in `pipeline/infrastructure.py` with correct account and region
- Update `pipeline_env` in `app.py` with correct account and region

```bash
npx cdk deploy AwsCdkSamChalice-Pipeline
```

## Delete all stacks
**Do not forget to delete the stacks to avoid unexpected charges**
```bash
npx cdk destroy AwsCdkSamChalice-Dev/Application
npx cdk destroy AwsCdkSamChalice-Pipeline
npx cdk destroy AwsCdkSamChalice-Pipeline/AwsCdkSamChalice-PreProd/Application
```

## Testing the web API
Below are examples that show the available resources and how to use them:
```bash
curl \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"username":"john", "email":"john@example.com"}' \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users

curl \
    -H "Content-Type: application/json" \
    -X GET \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users/john

curl \
    -H "Content-Type: application/json" \
    -X PUT \
    -d '{"country":"US", "state":"WA"}' \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users/john

curl \
    -H "Content-Type: application/json" \
    -X DELETE \
    https://API_ID.execute-api.REGION.amazonaws.com/v1/users/john
```
