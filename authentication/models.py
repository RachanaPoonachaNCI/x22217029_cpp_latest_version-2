from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    upload_to = 's3://x22217029-energy-tracker/profile_pictures/'
    
# Create your models here.
class consumer(models.Model):
    id = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50, null=True, default=None)
   # pp = models.ImageField(upload_to="uploads", null=True, default=None)
    pp = models.ImageField(upload_to='', storage=S3MediaStorage, null=True, default=None)


class airConditioner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(consumer, on_delete=models.CASCADE)
    watts = models.IntegerField()
