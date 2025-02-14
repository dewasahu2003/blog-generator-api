

# 🤖 AI Blog Generator with Amazon Bedrock

Generate AI-powered blog content automatically using Amazon Bedrock, AWS Lambda, and S3.
[Linkedin Post](https://www.linkedin.com/posts/dewasahu_aws-buildinpublic-awscommunity-activity-7296266731554004992-Upak?utm_source=share&utm_medium=member_desktop&rcm=ACoAADkObhwBfE_QsbN1RuFm0RkPTRMCOtFqZtw)

## 🔧 Architecture

![Architecture Diagram](https://github.com/user-attachments/assets/65be3146-bcf3-4e0e-b235-5dc16d2eecb1)

## ✨ Features

- 🧠 Automated blog generation using Llama 3 AI model
- ☁️ Serverless architecture with AWS Lambda
- 💾 Persistent storage in Amazon S3
- 🌐 RESTful API interface through API Gateway
- 📈 Scalable and cost-efficient design

## 🏗️ Architecture Overview

The system works in four simple steps:
1. 📥 Receive blog topic through API Gateway
2. ✍️ Generate content using Amazon Bedrock
3. 💾 Store the blog in Amazon S3
4. 📤 Return the storage location to the user

## 📋 Prerequisites

- ☁️ AWS Account with access to:
  - 🤖 Amazon Bedrock
  - ⚡ AWS Lambda
  - 💾 Amazon S3
  - 🌐 API Gateway
- 📚 Basic understanding of AWS services
- 💻 AWS CLI installed (optional)

## 🚀 Setup Instructions

### 1. Create S3 Bucket

1. 👉 Navigate to AWS S3 Console
2. ➕ Click "Create bucket"
3. ✏️ Enter a unique bucket name
4. ⚙️ Keep default settings
5. 💾 Click "Create bucket"

### 2. Deploy Lambda Function

1. 👉 Go to AWS Lambda Console
2. ➕ Click "Create function"
3. 📝 Select "Author from scratch"
4. 🐍 Choose Python runtime
5. 🔑 Set up IAM role with permissions for:
   - 💾 S3 (read/write)
   - 🤖 Bedrock (invoke model)
6. 📋 Copy the project's Lambda code
7. 🚀 Deploy the function

### 3. Configure API Gateway

1. 👉 Open API Gateway Console
2. ➕ Create new REST API
3. 📝 Add POST route `/bloggen`
4. 🔗 Connect to Lambda function
5. 🚀 Deploy API to a stage (e.g., "v1")

## 🧪 Testing the API

Use either curl or Postman to test:

```bash
curl -X POST \
  https://your-api-url/v1/bloggen \
  -H "Content-Type: application/json" \
  -d '{"blogtopic": "Future of AI"}'
```

Expected response:
```json
{
  "status": "success",
  "file_path": "s3://your-bucket/blogs/future-of-ai.md"
}
```

## ⚠️ Error Handling

The API handles common errors including:
- ❌ Invalid blog topics
- 🚫 AI generation failures
- 💥 S3 storage issues

Each error returns an appropriate HTTP status code and message.

## 🔒 Security

- 🛡️ API Gateway provides request throttling
- 🔐 Lambda executes in a secure VPC
- 🗄️ S3 bucket configured with appropriate permissions
- 👮 IAM roles follow least-privilege principle

## 👥 Contributing

1. 🔄 Fork the repository
2. 🌿 Create a feature branch
3. 💾 Commit changes
4. 🚀 Push to the branch
5. 📝 Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
