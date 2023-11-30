import boto3

session = boto3.session.Session()
        sqs_client = session.client('sqs')
        response = sqs_client.get_queue_url(QueueName=queue_name)
        queue_url = response['QueueUrl']
        print('\n==>message to send to the queue {} ...\n'.format(message))
        response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)