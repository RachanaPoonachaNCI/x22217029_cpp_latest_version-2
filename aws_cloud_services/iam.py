import boto3
from s3_credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Setting IAM user name for storage
IAM_USER_NAME = 's3'

# Creating an IAM client
iam = boto3.client('iam', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Attaching the policy to the IAM user
iam.attach_user_policy(
    UserName=IAM_USER_NAME,
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess' 
)

print(f"Policy has been attached to : {IAM_USER_NAME}")
