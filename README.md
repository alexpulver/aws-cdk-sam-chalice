# Example project for working with AWS CDK, AWS SAM and AWS Chalice

This project shows how AWS CDK and AWS Chalice can be used
together to deliver a service using CDK for building the broader service
infrastructure, and Chalice as developer-friendly Python serverless 
microframework.

The service being built is based on Amazon API Gateway and AWS Lambda, 
and provides basic CRUD operations for managing users in a DynamoDB table.

#### Setting up development environment

See [Getting Started With the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
for additional details and prerequisites

```bash
# Clone the code
git clone -b future https://github.com/alexpulver/aws-cdk-sam-chalice
cd aws-cdk-sam-chalice

# Create Python virtual environment and install the dependencies
python3 -m venv .venv
source .venv/bin/activate
scripts/install-deps.sh

## Upgrading dependencies (ordered by constraints)
pip-compile --upgrade api/runtime/requirements.in
pip-compile --upgrade requirements.in
pip-compile --upgrade requirements-dev.in
scripts/install-deps.sh
```

#### Synthesize and deploy development stack

The `AwsCdkSamChalice-Dev-Application` stack uses your current AWS profile account and credentials.

```bash
npx cdk synth
npx cdk deploy AwsCdkSamChalice-Dev-Application
```

Example output for `npx cdk deploy AwsCdkSamChalice-Dev-Application` stack:

```text
AwsCdkSamChalice-Dev-Application.UsersTableName = AwsCdkSamChalice-Dev-Application-UsersTable9725E9C8-BTQT7EIOV1UC
AwsCdkSamChalice-Dev-Application.APIHandlerArn = arn:aws:lambda:eu-west-1:123456789012:function:AwsCdkSamChalice-Dev-Application-APIHandler-13LVIC507UIAN
AwsCdkSamChalice-Dev-Application.APIHandlerName = AwsCdkSamChalice-Dev-Application-APIHandler-13LVIC507UIAN
AwsCdkSamChalice-Dev-Application.RestAPIId = letbml5594
AwsCdkSamChalice-Dev-Application.EndpointURL = https://letbml5594.execute-api.eu-west-1.amazonaws.com/v1/
```

**Do not forget to delete the stack once done with testing to avoid unexpected
charges:**
```bash
npx cdk destroy AwsCdkSamChalice-Dev-Application
```

#### Testing the web API

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
