from django.db import models
class patient(models.Model):
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField(max_length=12)
    desc=models.TextField()
    img1=models.ImageField(null=True,blank=True,upload_to="static/images/")
    img2=models.ImageField(null=True,blank=True,upload_to="static/images/")
    res1=models.CharField(max_length=22)
    res2=models.CharField(max_length=22)
    date=models.DateField()