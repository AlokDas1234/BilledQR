from django.db import models

# Create your models here.
class Item(models.Model):
    item_code = models.CharField(max_length=100,null=True,blank=True)
    item_name= models.CharField(max_length=100,null=True,blank=True)
    stock_qty= models.IntegerField(null=True,blank=True)

class validQrCode(models.Model):
    valid_qr=models.BooleanField(default=True,null=True,blank=True)

