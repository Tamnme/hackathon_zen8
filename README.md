# Gemini Lambda Function

This is a Dockerized AWS Lambda function that uses Google's Gemini API to summarize text.

## Prerequisites

- Docker
- AWS CLI configured with appropriate permissions
- AWS ECR repository
- Gemini API key

## Building the Docker Image

1. Build the Docker image:
```bash
docker build -t gemini-lambda .
```

2. Tag the image for ECR:
```bash
docker tag gemini-lambda:latest <your-account-id>.dkr.ecr.<region>.amazonaws.com/gemini-lambda:latest
```

3. Push to ECR:
```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<region>.amazonaws.com
docker push <your-account-id>.dkr.ecr.<region>.amazonaws.com/gemini-lambda:latest
```

## Environment Variables

The function requires the following environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key

## Lambda Configuration

1. Create a new Lambda function using the container image
2. Set the environment variable `GEMINI_API_KEY`
3. Configure appropriate memory and timeout settings (recommended: 512MB memory, 30s timeout)

## Testing Locally

You can test the function locally using the AWS Lambda runtime interface:

```bash
docker run -p 9000:8080 -e GEMINI_API_KEY=your_api_key gemini-lambda:latest
```

Then test with curl:
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"text": "Your text to summarize"}'
```

## Input Format

The function expects a JSON input with the following structure:
```json
{
    "text": "Text to summarize",
    "custom_prompt": "Optional custom prompt"
}
```

The API key can be provided either:
- In the event: `{"api_key": "your_key", "text": "..."}`
- As an environment variable: `GEMINI_API_KEY`