from django.db import models
from Home.models import DoctorProfile, UserProfile, HospitalProfile,ReceiverProfile
from django.contrib.auth.models import User


class Consutation(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete = models.SET_NULL, null = True)
    hospitel = models.ForeignKey(HospitalProfile, on_delete = models.SET_NULL, null = True)
    patient = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    date = models.DateField(auto_now_add = False)
    time = models.TimeField(auto_now_add = False)
    approval = models.BooleanField(default = False)

    def __str__(self):
        return "consultaion on " + str(self.date) + " at " + str(self.time) + "doctor " + str(self.doctor) 




class OrganDonation(models.Model):
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
    options1 = (("Kidneys","Kidneys"),("Liver","Liver"),("Lungs","Lungs"),("Heart","Heart"),("Pancreas","Pancreas"),("Intestines","Intestines"),("Hands","Hands"),("Eye","Eye"))

    doner = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True)
    organ = models.CharField(max_length = 255, choices=options1)
    Bloodgroup = models.CharField(max_length=255, choices= options)
    HealthPath = models.CharField(max_length = 1000)
    Hospital = models.ForeignKey(HospitalProfile, on_delete = models.SET_NULL, null = True)
    availability = models.BooleanField(default = True)

    def __str__(self):
        return "ORGAN " + str(self.organ) + " DONER " + str(self.doner) + "Hospital " + str(self.Hospital)

class Organrequest(models.Model):
    # Organ = models.ForeignKey(OrganDonation,on_delete = models.CASCADE)
    options = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))

    options1 = (("Kidneys", "Kidneys"), ("Liver", "Liver"), ("Lungs", "Lungs"), ("Heart", "Heart"), ("Pancreas", "Pancreas"), ("Intestines", "Intestines"), ("Hands", "Hands"), ("Eye", "Eye"))
    organ = models.CharField(max_length=255, choices=options1)
    doctor = models.ForeignKey(DoctorProfile, on_delete = models.SET_NULL, null = True, related_name="doctor_for_request")
    Donar = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True,blank=True)
    Donar_approval = models.BooleanField(default = False)
    Bloodgroup = models.CharField(max_length=255, choices= options)
    patient = models.ForeignKey(ReceiverProfile, on_delete = models.CASCADE)
    request_status = models.BooleanField(default = True)
    HealthRecord = models.FileField(upload_to="HealthFile")
    is_healthrecord_status = models.BooleanField(default=False)
    approval_status = models.BooleanField(default = False)
    status = models.CharField(max_length=20, default="Pending",choices=(("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")))
    date = models.DateField(auto_now = True)

    def __str__(self):
        return "ORGAN request by" + str(self.doctor) + " Organ " + str(self.organ) + "Patient " + str(self.patient)


class Surgery(models.Model):
    # consultaion = models.ForeignKey(Consutation,on_delete = models.CASCADE)
    organrequest = models.ForeignKey(Organrequest,on_delete = models.CASCADE,null=True)
    patient = models.ForeignKey(ReceiverProfile, on_delete = models.CASCADE)
    donar = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    surgery_date = models.DateField(auto_now_add = False)
    admint_date = models.DateField(auto_now_add = False)
    surgery_status = models.BooleanField(default = False)
    comments_doctor = models.CharField(max_length = 1000, null= True)
    completion_status = models.BooleanField(default = False)
    
    def __str__(self):
        return "Surgery Planed for" + str(self.patient) + " Organ " + str(self.organrequest) + "Date " + str(self.surgery_date)

    
