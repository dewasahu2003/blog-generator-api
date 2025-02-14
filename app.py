import boto3
import botocore.config
import json
import time
import logging
from datetime import datetime

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# init bedrock client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name="ap-south-1",
    config=botocore.config.Config(read_timeout=60, retries={"max_attempts": 3}),
)

def blog_generate_using_bedrock(blogtopic: str) -> str:
    # generate blog with bedrock ai
    prompt = f"<s>[INST]Human: Write a 200-word blog on {blogtopic}\nAssistant:[/INST]"
    
    body = {
        "prompt": prompt,
        "max_gen_len": 256,  # faster response
        "temperature": 0.7,
        "top_p": 0.9,
    }

    try:
        start_time = time.time()  # start timer

        response = bedrock.invoke_model(
            body=json.dumps(body),
            modelId="meta.llama3-8b-instruct-v1:0",
            accept="application/json",
            contentType="application/json",
        )

        elapsed_time = time.time() - start_time  # get response time
        logger.info(f"Bedrock API response time: {elapsed_time:.2f} seconds")

        # process response
        response_content = response.get("body").read().decode("utf-8")
        logger.info(f"Raw Bedrock Response: {response_content}")

        # get blog text
        response_body = json.loads(response_content)
        blog = response_body["generation"].strip()
        
        return blog

    except botocore.exceptions.ClientError as e:
        logger.error(f"Bedrock API error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in blog generation: {str(e)}")
        return None


def save_blog_s3(key, body):
    # save to s3
    try:
        s3 = boto3.client("s3")
        s3.put_object(Bucket="sagemakermobbucket555", Key=key, Body=body)
        logger.info(f"Blog successfully saved to S3: {key}")
        return True
    except Exception as e:
        logger.error(f"S3 Error: {str(e)}")
        return False


def lambda_handler(event, context):
    # main lambda function
    try:
        # get request data
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event.get("body", {})

        # check topic
        blogtopic = body.get("blogtopic")
        if not blogtopic:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "blogtopic is required"}),
            }

        # make blog
        blog = blog_generate_using_bedrock(blogtopic)
        if blog:
            curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            s3_key = f"blogs/{blogtopic}-{curr_time}.txt"

            # save to s3
            if save_blog_s3(s3_key, blog):
                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {"message": "Blog generated successfully", "s3_key": s3_key}
                    ),
                }
            else:
                return {
                    "statusCode": 500,
                    "body": json.dumps({"error": "Failed to save blog to S3"}),
                }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to generate blog"}),
            }

    except Exception as e:
        logger.error(f"Lambda execution error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}