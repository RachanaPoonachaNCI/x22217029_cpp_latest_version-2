import json
import boto3
from datetime import datetime

def send_sqs_message(email):
    try:
        session = boto3.session.Session(region_name='eu-north-1')
        sqs_client = session.client('sqs')

        user_data = {
            'username': email,
            'timestamp': str(datetime.now())
        }
        # Convert user_data to JSON form
        message_body = json.dumps(user_data)

        print("Going to send to SQS")
        response = sqs_client.get_queue_url(QueueName='x22217029_cpp')
        queue_url = response['QueueUrl']

        print('==> Message to send to the queue: {}'.format("User has been registered successfully"))
        response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
        
        return True
    except Exception as e:
        print(f"Error while sending message to SQS: {e}")
        return False