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
pip install pip-tools==6.1.0  # [Optional] Needed to upgrade dependencies and cleanup unused packages
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
when upgrading AWS CDK packages version.

```bash
pip-compile --upgrade api/runtime/requirements.in
pip-compile --upgrade requirements.in
pip-compile --upgrade requirements-dev.in
./scripts/install-deps.sh
pip-sync api/runtime/requirements.txt requirements.txt requirements-dev.txt  # [Optional] Cleanup unused packages
./scripts/run-tests.sh
```

## Deploy the application to development environment
The `AwsCdkSamChalice-Dev` deployment uses your default account and region.
It consists of two stacks - stateful (database) and stateless (API and monitoring) 

```bash
npx cdk deploy "AwsCdkSamChalice-Dev/*"
```

Example outputs for `npx cdk deploy "AwsCdkSamChalice-Dev/*"`:
```text
 ✅  AwsCdkSamChaliceDevStateful7B33C11B (AwsCdkSamChalice-Dev-Stateful)

Outputs:
AwsCdkSamChaliceDevStateful7B33C11B.ExportsOutputFnGetAttDatabaseTableF104A135ArnDAC15A6A = arn:aws:dynamodb:eu-west-1:807650736403:table/AwsCdkSamChalice-Dev-Stateful-DatabaseTableF104A135-1LVXRPCPOKVZQ
AwsCdkSamChaliceDevStateful7B33C11B.ExportsOutputRefDatabaseTableF104A1356B7D7D8A = AwsCdkSamChalice-Dev-Stateful-DatabaseTableF104A135-1LVXRPCPOKVZQ
```
```text
 ✅  AwsCdkSamChaliceDevStateless0E5B7E4B (AwsCdkSamChalice-Dev-Stateless)

Outputs:
AwsCdkSamChaliceDevStateless0E5B7E4B.APIHandlerArn = arn:aws:lambda:eu-west-1:807650736403:function:AwsCdkSamChalice-Dev-Stateless-APIHandler-PJjw0Jn7Waq0
AwsCdkSamChaliceDevStateless0E5B7E4B.APIHandlerName = AwsCdkSamChalice-Dev-Stateless-APIHandler-PJjw0Jn7Waq0
AwsCdkSamChaliceDevStateless0E5B7E4B.EndpointURL = https://zx5s6bum21.execute-api.eu-west-1.amazonaws.com/v1/
AwsCdkSamChaliceDevStateless0E5B7E4B.RestAPIId = zx5s6bum21
```

## Deploy the pipeline
**Prerequisites**
- Fork the repository and create AWS CodeStar Connections [connection](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html) for it
- Update `source_action` in `pipeline.py` with the connection, owner and repository details from previous step
- Update `pre_prod_env` in `pipeline.py` with correct account and region
- Update `pipeline_env` in `app.py` with correct account and region

```bash
npx cdk deploy AwsCdkSamChalice-Pipeline
```

## Delete all stacks
**Do not forget to delete the stacks to avoid unexpected charges**
```bash
npx cdk destroy "AwsCdkSamChalice-Dev/*"
npx cdk destroy AwsCdkSamChalice-Pipeline
npx cdk destroy "AwsCdkSamChalice-Pipeline/AwsCdkSamChalice-PreProd/*"
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
