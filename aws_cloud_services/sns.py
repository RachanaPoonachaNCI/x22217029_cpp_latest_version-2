import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnsWrapper:

    def __init__(self, sns_client, sns_resource):
        self.sns_client = sns_client
        self.sns_resource = sns_resource


    def create_topic(self, name):
        try:
            topic = self.sns_resource.create_topic(Name=name)
            logger.info("Created topic %s with ARN %s.", name, topic.arn)
        except ClientError:
            logger.exception("Couldn't create topic %s.", name)
            raise
        else:
            return topic
            
region = 'eu-west-1'

    # Create an SNS client and resource
sns_client = boto3.client('sns', region_name=region)
sns_resource = boto3.resource('sns', region_name=region)

sns_wrapper = SnsWrapper(sns_client, sns_resource)

    # Specify the desired topic name
topic_name = 'x22217029_energy_tracker'

try:
# Call the create_topic method
    topic = sns_wrapper.create_topic(topic_name)
    print(f"Topic ARN: {topic.arn}")
except Exception as e:
    print(f"Error creating topic: {e}")



# def send_sns_notification(email, message):
#     # Replace 'your-aws-access-key-id' and 'your-aws-secret-access-key' with your AWS credentials
#     aws_access_key_id = 'your-aws-access-key-id'
#     aws_secret_access_key = 'your-aws-secret-access-key'
    
#     # Replace 'your-sns-topic-arn' with your SNS topic ARN
#     sns_topic_arn = 'your-sns-topic-arn'
    
#     # Create an SNS client
#     sns = boto3.client('sns', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='your-region')
    
#     # Send a message to the specified SNS topic
#     sns.publish(TopicArn=sns_topic_arn, Message=message, Subject=f"Signup Success: {email}")