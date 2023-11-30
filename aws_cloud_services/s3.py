import boto3
import warnings

warnings.simplefilter('ignore')
s3 = boto3.client('s3')
bucket_name = 'x22217029-energy-tracker-cpp'
s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
print(bucket_name)
# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]
print("Bucket List: %s" % buckets)