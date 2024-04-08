from django.shortcuts import render, redirect 
from django.contrib import messages
from Home.models import DoctorProfile, UserProfile, HospitalProfile
from .forms  import ConsultaionAdd, AddOrganDonation, OrganDonationRequest, SurgeyAdd
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
    surgery = Surgery.objects.filter(patient__user = request.user)
    context = {
        "surgery":surgery
    }
    return render(request,"surgery.html",context)


def DoctorConsultaion(request):
    consultation = Consutation.objects.filter(doctor__user = request.user)

    context = {
        "consultation":consultation
    }
    return render(request,"doctorconsultaion.html",context)

def ApproveConsultationrequest(request,pk):
    consutation = Consutation.objects.get(id = pk)
    consutation.approval = True 
    consutation.save()
    messages.info(request,"Request approved...")
    return redirect("DoctorConsultaion")


def DoctorSurgery(request):
    surgey = Surgery.objects.filter(organrequest__doctor__user = request.user)

    context = {
        "surgey":surgey
    }
    return render(request,"doctorsurgery.html",context)


def Addsurgery(request,pk):
    organrequest = Organrequest.objects.get(id = pk)
    form = SurgeyAdd()
    if request.method == "POST":
        form = SurgeyAdd(request.POST)
        if form.is_valid():
            surgery = form.save()
            surgery.organrequest = organrequest
            surgery.save()
            return redirect()

    context = {
        "form":form
    }
    return render(request,"addsurgery.html",context)

def DoctordonationView(request):
    donation = OrganDonation.objects.all()
    donationrequest = Organrequest.objects.filter(doctor = DoctorProfile.objects.get(user  = request.user))

    context = {
        "donation":donation,
        "donationrequest":donationrequest
    }
    return render(request,"organdoners.html",context)

def OrganDonationAdd(request):
    form = AddOrganDonation()

    if request.method == "POST":
        form = AddOrganDonation(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Organ Addedd........")
            return redirect("DoctordonationView")
        else:
            messages.info(request,"Something Wrong........")
            return redirect("DoctordonationView")


    context = {
        "form":form
    }
    return render(request,'addorgan.html',context)


def AddOrganRequets(request):
    form = OrganDonationRequest()
    user = UserProfile.objects.all()

    if request.method == "POST":
        patient_id = request.POST["patientid"]
        profile = UserProfile.objects.get(id = str(patient_id))
       
        form = OrganDonationRequest(request.POST)
        if form.is_valid():
            organrequest = form.save()
            organrequest.patient =  profile
            organrequest.doctor = DoctorProfile.objects.get(user  = request.user)
            organrequest.save()
            messages.info(request,"Organ request Addedd........")
            return redirect("DoctordonationView")
        else:
            messages.info(request,"Something Wrong........")
            return redirect("DoctordonationView")

    context = {
        "form":form,
        "user":user
    }
    return render(request,"adddonationrequest.html",context)
