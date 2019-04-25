from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Warehouse(models.Model):
    w_id = models.IntegerField(primary_key = True)
    x = models.IntegerField()
    y = models.IntegerField()

class Truck(models.Model):
    truck_id = models.IntegerField(primary_key=True)
    x = models.IntegerField(null = True, blank = True)
    y = models.IntegerField(null = True, blank = True)
    status =  models.CharField(max_length=100,default="",null=True, blank=True)

class Package(models.Model):
    packageid = models.IntegerField(primary_key=True)
    truck = models.ForeignKey(Truck, on_delete = models.CASCADE,null=True,blank=True,related_name = "package_set")
    warehouse =  models.ForeignKey(Warehouse, on_delete = models.CASCADE,null=True,blank=True,related_name = "package_set")
    x = models.IntegerField(null = True, blank = True)
    y = models.IntegerField(null = True, blank = True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
class Product(models.Model):
    productid = models.IntegerField()
    description =  models.CharField(max_length=10000,default="",null=True, blank=True)
    amount = models.IntegerField()
    package =  models.ForeignKey(Package, on_delete = models.CASCADE,null=True,blank=True,related_name = "product_set")

    
class IncomingSeqWorld(models.Model):
    sequence_number = models.IntegerField(primary_key = True)

class OutgoingSeqWorld(models.Model):
    #Don't we need to save the message as well? To send it again?
    sequence_number = models.IntegerField(primary_key = True)
    acked = models.BooleanField(default = False)
    message =  models.CharField(max_length=10000,default="",null=True, blank=True)
    
class IncomingSeqUA(models.Model):
    sequence_number = models.IntegerField(primary_key = True)

class OutgoingSeqUA(models.Model):
    sequence_number = models.IntegerField(primary_key = True)
    acked = models.BooleanField(default = False)
    message =  models.CharField(max_length=10000,default="",null=True, blank=True)
