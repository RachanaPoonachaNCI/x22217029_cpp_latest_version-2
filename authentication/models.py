from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    location = 's3://x22217029-energy-tracker/'
    
# Create your models here.
class consumer(models.Model):
    id = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50, null=True, default=None)
    pp = models.CharField(max_length=50, null=True, default=None)
  #  def get_filename(self):
   #   return self.pp.name if self.pp else "default_profile_picture.png"


class airConditioner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(consumer, on_delete=models.CASCADE)
    watts = models.IntegerField()

