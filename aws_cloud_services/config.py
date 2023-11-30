import boto3
import json

def retrieve_secret(secret_name):
    secretsManager = boto3.client('secretsmanager')

    try:
        secret_response = secretsManager.get_secret_value(SecretId=secret_name)
        secret_data = json.loads(secret_response['SecretString'])
        return secret_data['your_password_key']
    except secretsManager.exceptions.ResourceNotFoundException:
        return None

if __name__ == "__main__":
    secretName = 'x22217029-energy-tracker-postgres-secret'  # Replace with your actual secret name
    password = retrieve_secret(secretName)

    if password:
        print(f"Password has been retrieved: {password}")
    else:
        print("Secret not found.")
