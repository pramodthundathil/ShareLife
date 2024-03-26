from django.shortcuts import render, redirect 
from django.contrib import messages
from Home.models import DoctorProfile, UserProfile, HospitalProfile
from .forms  import ConsultaionAdd, AddOrganDonation
from .models import Consutation, OrganDonation, Organrequest, Surgery

# Create your views here.

def GetAppoinment(request):
    form = ConsultaionAdd()
    if request.method == "POST":
        form = ConsultaionAdd(request.POST)
        if form.is_valid():
            consultation = form.save()
            consultation.patient = request.user
            consultation.save()
            messages.info(request,"consultaion Requested.........")
            return redirect("MyAppointments")

    context = {
        "form":form
    }
    return render(request,"getappoinment.html",context)


def MyAppointments(request):
    consultation = Consutation.objects.filter(patient = request.user)

    context = {
        "consultation":consultation
    }
    return render(request,"myappointments.html",context)


def Doctors(request):
    doctor = DoctorProfile.objects.all()

    context = {
        "doctor":doctor
    }

    return render(request,"doctors.html",context) 


def OrganDonations(request):
    donation = OrganDonation.objects.all()

    context = {
        "donation":donation,
        
    }
    return render(request,"donateorgan.html",context)




def Surgeryview(request):
    return render(request,"surgery.html")


def DoctorConsultaion(request):
    consultation = Consutation.objects.filter(doctor__user = request.user)

    context = {
        "consultation":consultation
    }
    return render(request,"doctorconsultaion.html",context)


def DoctorSurgery(request):
    surgey = Surgery.objects.filter(consultaion__doctor__user = request.user)

    context = {
        "surgey":surgey
    }
    return render(request,"doctorsurgery.html",context)

def DoctordonationView(request):
    return render(request,"organdoners.html")

def OrganDonationAdd(request):
    form = AddOrganDonation()

    context = {
        "form":form
    }
    return render(request,'addorgan.html',context)
