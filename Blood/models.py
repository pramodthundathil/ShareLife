from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BloodVault(models.Model):
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
    blood_group = models.CharField(max_length=20, choices=options)
    total_unit = models.IntegerField()
    updated_on = models.DateField(auto_now=True)


class BloodReceptRequests(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE, related_name="donation_request")
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
    requested_group = models.CharField(max_length=20, choices=options)
    unit = models.IntegerField()
    date = models.DateField(auto_now_add =True)
    updated_date = models.DateField(auto_now=True)
    approval = models.BooleanField(default=False)


class BloodDonation(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE, related_name="_request")
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
    donated_group = models.CharField(max_length=20, choices=options)
    unit = models.IntegerField()
    donated_date = models.DateField(auto_now_add=True)
    approval = models.BooleanField(default=False)










