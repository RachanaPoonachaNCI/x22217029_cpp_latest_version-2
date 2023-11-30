# Import necessary libraries
import boto3
import json
from botocore.exceptions import ClientError

# Function to retrieve the secret
def get_secret():
    # Specify the name of the secret in AWS Secrets Manager
    secret_name = "x22217029-energy-tracker-postgres-secret"
    
    # Specify the AWS region where the secret is stored
    region_name = "eu-west-1"

    # Create a Secrets Manager client using the specified region
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Attempt to retrieve the secret value using the specified secret name
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle exceptions if any occur during the retrieval
        # For a list of exceptions thrown, see the AWS documentation:
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypt the secret using the associated KMS key and retrieve the SecretString
    secret = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret)
    return secret_dict

#     # Your code goes here. In this example, the secret is returned, but you would typically
#     # parse the secret JSON or extract specific information as needed.

#     return secret

# # Call the function to retrieve the secret
# retrieved_secret = get_secret()

# # Optionally, print or use the retrieved secret in your application
# print(retrieved_secret)
