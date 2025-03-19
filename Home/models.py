from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(models.Model):
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(auto_now_add = False)
    Bloodgroup = models.CharField(max_length=255, choices= options)
    Address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="profilepic")
    medical_doc= models.FileField(upload_to="documents", null=True, blank=True)
    user = models.OneToOneField(User,on_delete = models.CASCADE,null = True, related_name='profile')

    def __str__(self):
        return str(self.user.first_name) + "  " +str(self.last_name)  + f" Blood Group {self.Bloodgroup}"
   

class ReceiverProfile(models.Model):
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    Bloodgroup = models.CharField(max_length=255, choices= options)
    last_name = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="profilepic")
    medical_doc= models.FileField(upload_to="documents", null=True, blank=True)
    active = models.BooleanField(default = False)


    def __str__(self):
        return str(self.user.first_name) + " " + str(self.last_name) + " Reciter"



class Block_1(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(User,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    Blockhash = models.CharField(max_length=255)
    
class Block_2(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(Block_1,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    MedicineBlock = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    Blockhash = models.CharField(max_length=255)
 
class Block_3(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(Block_2,on_delete=models.CASCADE)
    MedicineBlock = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    Blockhash = models.CharField(max_length=255)
    
class Block_4(models.Model):
    BlockIndex = models.CharField(max_length=20)
    BlockTimeStrap = models.DateTimeField(auto_now_add=True)
    BlockData = models.CharField(max_length=255)
    BlockLink = models.ForeignKey(Block_3,on_delete=models.CASCADE)
    MedicineBlock = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    previous_hash = models.CharField(max_length=255)
    Blockhash = models.CharField(max_length=255)

    
class HospitalProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    name = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="profilepic")
    active = models.BooleanField(default = False)


    def __str__(self):
        return str(self.name) + " Hospital"
    

class DoctorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True, related_name='doctor')
    last_name = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    Specilisation = models.CharField(max_length=255)
    profile_pic = models.FileField(upload_to="profilepic")
    active = models.BooleanField(default = False)
    hospital = models.ForeignKey(HospitalProfile,on_delete=models.CASCADE,null=True, blank=True) 
    

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.Specilisation) + " " + str(self.hospital)
    


    
