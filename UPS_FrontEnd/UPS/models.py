from django.db import models

# Create your models here.
class Warehouse(models.Model):
    w_id = models.IntegerField(primary_key = True)
    x = models.IntegerField()
    y = models.IntegerField()

class Truck(models.Model):
    truck_id = models.IntegerField(primary_key=True)
    status =  models.CharField(max_length=100,default="",null=True, blank=True)

class Package(models.Model):
    packageid = models.IntegerField(primary_key=True)
    truck = models.ForeignKey(Truck, on_delete = models.CASCADE,null=True,blank=True,related_name = "package_set")
    
class IncomingSeqWorld(models.Model):
    sequence_number = models.IntegerField(primary_key = True)

class OutgoingSeqWorld(models.Model):
    sequence_number = models.IntegerField(primary_key = True)
    acked = models.BooleanField(default = False)
    
class IncomingSeqUA(models.Model):
    sequence_number = models.IntegerField(primary_key = True)

class OutgoingSeqUA(models.Model):
    sequence_number = models.IntegerField(primary_key = True)
    acked = models.BooleanField(default = False)

    
