## Example project for working with AWS CDK, AWS SAM and AWS Chalice

This project shows how AWS CDK, AWS SAM and AWS Chalice can be used
together to deliver a service using CDK for building the broader service
infrastructure, Chalice as developer-friendly Python serverless 
microframework and SAM as integration point between the two.

The service is based on Amazon API Gateway and AWS Lambda. 
The web API provides basic CRUD operations for managing users in a 
DynamoDB table.

### Setting up development environment

See [Getting Started With the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
for additional details and prerequisites

```bash
# Install the CDK CLI
npm install -g aws-cdk

# Clone the code
git clone https://github.com/alexpulver/aws-cdk-sam-chalice
cd aws-cdk-sam-chalice

# Create Python virtual environment and install the dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r infra/requirements.txt
pip install -r web-api/requirements.txt
```

### Synthesize and deploy development stack

The `WebApiDev` stack uses your current AWS profile account and credentials.

```bash
cd infra
cdk synth
cdk deploy WebApiDev
```

Example output for `cdk deploy ...`:

```text
WebApiDev.UsersTableName = WebApiDev-UsersTable9725E9C8-BTQT7EIOV1UC
WebApiDev.APIHandlerArn = arn:aws:lambda:eu-west-1:123456789012:function:WebApiDev-APIHandler-13LVIC507UIAN
WebApiDev.APIHandlerName = WebApiDev-APIHandler-13LVIC507UIAN
WebApiDev.RestAPIId = letbml5594
WebApiDev.EndpointURL = https://letbml5594.execute-api.eu-west-1.amazonaws.com/v1/
```

**Do not forget to delete the stack once done with testing to avoid unexpected
charges:**
```bash
cdk destroy WebApiDev
```

### Testing the web API

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
