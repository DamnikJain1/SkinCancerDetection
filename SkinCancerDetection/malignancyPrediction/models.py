from django.db import models

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    speciality = models.CharField(max_length=50)
    address = models.CharField(max_length=60)
    pincode= models.CharField(max_length=10)

    def __unicode__(self):
        return self.first_name
        return self.last_name
        return self.speciality
        return self.address
        return self.pincode

# Create your models here.
class Forum(models.Model):
    sent_by = models.CharField(max_length=30)
    message = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return self.sent_by
        return self.message
