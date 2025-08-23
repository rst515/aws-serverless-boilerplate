# AWS Serverless Boilerplate

A serverless application boilerplate built with AWS SAM, demonstrating best practices for serverless development.

## Features

- AWS Lambda with Python 3.11
- AWS SAM for infrastructure as code
- DynamoDB integration
- API Gateway endpoints
- AWS Lambda Powertools integration
- Comprehensive logging and tracing
- Unit testing with moto
- Type checking with mypy
- Code quality with pylint

## Architecture

The application follows a serverless architecture pattern:

- API Gateway for HTTP endpoints
- Lambda functions for business logic
- DynamoDB for data persistence
- AWS Lambda Powertools for observability

## Prerequisites

- Python 3.11
- AWS SAM CLI
- AWS CLI configured with appropriate credentials
- Docker (for local testing)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirement.txt
```
3. Set up Python locally (recommended with pyenv) and a virtual environment:
```bash
pyenv install -s 3.11.9 pyenv local 3.11.9 python -m venv .venv source .venv/bin/activate 
```
4. Initialize and build the SAM application:
```bash
sam build
```
5. Configure your AWS credentials (if not already):
```bash
aws configure
```
6. Deploy to AWS (first time with guided prompts):
```bash
sam deploy --guided
```

## Local development

- Start the local API (requires Docker running):
```bash
sam local start-api
```
The API will be available at http://127.0.0.1:3000
- Invoke a function locally with an event:
```bash
sam local invoke -e events/sample.json
```
- Tail CloudWatch logs for a function in the deployed stack:
```bash
sam logs -n --stack-name --tail
```

## Configuration
- Environment variables: define them in template.yaml for each function or provide a file for local runs:
  - For local runs, create an env.json:
```json
{ "Parameters": {}, "Environment": { "Variables": { "LOG_LEVEL": "INFO", "TABLE_NAME": "your-table-name" } } }
```
  - Then run:
```bash
sam local start-api --env-vars env.json
```
  - Parameters: use SAM parameters in template.yaml and override on deploy:
```bash
sam deploy --parameter-overrides TableName=your-table-name Stage=dev
```

## Testing

- Run unit tests, linting, security and other code quality checks:
```bash
tools/dev/pre_push.sh
```


## Project structure

A typical layout for this project:  
```
├─ src/ # Lambda source code  
├─ tests/ # Unit tests  
├─ events/ # Sample event payloads for local testing  
├─ template.yaml # SAM template  
├─ requirements.txt # Python dependencies  
└─ README.md
```

## Deployment

- Build:
```bash
sam build
```

- Deploy (guided on first run, then non-guided):
```bash
sam deploy
# or with specific params
sam deploy --stack-name serverless-boilerplate --capabilities CAPABILITY_IAM --parameter-overrides Stage=prod

```