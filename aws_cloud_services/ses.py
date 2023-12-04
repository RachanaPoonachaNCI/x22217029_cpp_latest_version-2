import json
import boto3
SES_CLIENT = boto3.client("ses")
SENDER = "cpp.new.project@gmail.com"
RECIPIENT = "rachna.kottangada.92@gmail.com"

def lambda_handler(event, context):
    print("Method executed")
    if 'Records' in event and event['Records']:
        # Records found, send email with content
        message = event['Records'][0]['body']
        subject = "New user registered"
        body = "User details: " + message
        response = SES_CLIENT.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        return "Email notification sent for received records"
    else:
        # If no records found
        subject = "SQS Message Received Without Records"
        body = "A message was received on the queue, but no records were found."
        response = SES_CLIENT.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        return "Email notification sent for no records in the event"
