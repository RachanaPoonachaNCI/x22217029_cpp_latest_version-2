import boto3

AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'

# Set your IAM user name
IAM_USER_NAME = 'your-iam-user-name'

# Create an IAM client
iam = boto3.client('iam', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Attach the policy to the IAM user
iam.attach_user_policy(
    UserName=IAM_USER_NAME,
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'  # Replace with the desired policy ARN
)

print(f"Policy attached to IAM user: {IAM_USER_NAME}")
