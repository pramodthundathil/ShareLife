from django.shortcuts import render, redirect 
from django.contrib import messages
from Home.models import DoctorProfile, UserProfile, HospitalProfile, ReceiverProfile
from .forms  import ConsultaionAdd, AddOrganDonation, OrganDonationRequest, SurgeyAdd
from .models import Consutation, OrganDonation, Organrequest, Surgery
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.

def GetAppoinment(request):
    form = ConsultaionAdd()
    if request.method == "POST":
        form = ConsultaionAdd(request.POST)
        if form.is_valid():
            consultation = form.save()
            consultation.patient = request.user
            consultation.hospitel = consultation.doctor.hospital
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
    donation = Organrequest.objects.filter(Donar__user = request.user )

    context = {
        "donation":donation,
        
    }
    return render(request,"donateorgan.html",context)




def Surgeryview(request):
    surgery = Surgery.objects.filter(patient__user = request.user)
    donationrequest = Organrequest.objects.filter(Organ__doner__user = request.user)
    context = {
        "surgery":surgery,
        "donationrequest":donationrequest
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
            return redirect("Addsurgery", pk= pk)

    context = {
        "form":form
    }
    return render(request,"addsurgery.html",context)

def DoctordonationView(request):
    donation = OrganDonation.objects.all()
    donars = User.objects.filter(groups=None, is_active = False)
    donationrequest = Organrequest.objects.filter(doctor = DoctorProfile.objects.get(user  = request.user))

    context = {
        "donation":donation,
        "donationrequest":donationrequest,
        "donars":donars
    }
    return render(request,"organdoners.html",context)


def DoctordonationView_approved(request):
    donars = User.objects.filter(groups=None, is_active = True)
    context = {
        
        "donars":donars
    }
    return render(request,"organdoners_approved.html",context)




def OrganDonationAdd(request):
    form = AddOrganDonation()
    users = UserProfile.objects.all()

    if request.method == "POST":
        form = AddOrganDonation(request.POST)
        user = request.POST.get("doner")
        blood = request.POST.get("bloodgroup")
        if form.is_valid():
            donation = form.save()
            donation.doner = UserProfile.objects.get(id = int(user))
            donation.Bloodgroup =  blood
            donation.save() 
            messages.info(request,"Organ Addedd........")
            return redirect("OrganDonations")
        else:
            messages.info(request,"Organ not Addedd........")
            return redirect("OrganDonations")
       
           


    context = {
        "form":form,
        "users":users
    }
    return render(request,'addorgan.html',context)


def getbloodgroup(request, donor_id):
    try:
        donor = UserProfile.objects.get(id=donor_id)
        blood_group = donor.Bloodgroup  # Assuming the field name is 'blood_group', adjust it if necessary
        return JsonResponse({'success': True, 'bloodGroup': blood_group})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False})


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


def ConsultationrequestsHospitels(request):
    consultation = Consutation.objects.filter(hospitel__user = request.user )

    context = {
        "consultation":consultation
    }
    return render(request,"counsultaionreq.html",context)


def SurgeryHospital(request):
    surgey = Surgery.objects.filter(organrequest__hospitel__user = request.user)
    context = {
        "surgey":surgey
    }
    return render(request,"surgeryHospital.html",context)

def OrganDonationHospital(request):
    donation = OrganDonation.objects.all()
    context = {
        "donation":donation
    }
    return render(request,"donnershospital.html",context)

def UploadRecord(request,pk):
    donerrequest = Organrequest.objects.get(id = pk)
    if request.method == "POST":
        record = request.FILES['record']
        donerrequest.HealthRecord = record
        donerrequest.is_healthrecord_status = True
        donerrequest.save()
        messages.info(request,"Health Record Uploaded....")
        return redirect("Surgeryview")
    return redirect("Surgeryview")


def OrgandonationRequests(request):
    form = OrganDonationRequest()
    user = ReceiverProfile.objects.get(user = request.user)
    r_requests = Organrequest.objects.filter(patient = user)
    

    if request.method == "POST":
        form = OrganDonationRequest(request.POST, request.FILES)
        if form.is_valid():
            organrequest = form.save(commit=False)
            organrequest.patient = user
            organrequest.Bloodgroup = user.Bloodgroup
            organrequest.save()
            messages.info(request,"Organ request Addedd........")
            return redirect("OrgandonationRequests")
        else:
            messages.info(request,"Something Wrong........")
            return redirect("OrgandonationRequests")
    context = {
        "form":form,
        "r_requests":r_requests
    }
    return render(request, "receverrequests.html",context)


def Recever_requestsDoctor(request):
    user = DoctorProfile.objects.get(user = request.user)
    r_requests = Organrequest.objects.filter(doctor = user)

    context = {
        "r_requests":r_requests
    }
    return render(request, 'receiver_request_doctor.html', context)


def view_receiver_request_doctor(request, pk):


    context = {
        "request":Organrequest.objects.get(id = pk),
        "donars":UserProfile.objects.all()
    }
    return render(request, 'view_receiver_request_doctor.html',context)

def assign_donar(request, pk):
    if request.method == "POST":
        donar_id = request.POST.get("donar")
        organ_request = Organrequest.objects.get(id=pk)
        organ_request.Donar = UserProfile.objects.get(id=donar_id)
       
        organ_request.save()
        messages.success(request, "Donor assigned successfully.")
        return redirect("view_receiver_request_doctor", pk=pk)


def organ_approve(request, pk):
    try:
        organ_request = Organrequest.objects.get(id=pk)
        organ_request.status = "Approved"
        organ_request.save()
        messages.success(request, "Request approved successfully.")
    except Organrequest.DoesNotExist:
        messages.error(request, "Request not found.")
    return redirect("Recever_requestsDoctor")


def reject_request(request, pk):
    try:
        organ_request = Organrequest.objects.get(id=pk)
        organ_request.status = "Rejected"
        organ_request.save()
        messages.success(request, "Request rejected successfully.")
    except Organrequest.DoesNotExist:
        messages.error(request, "Request not found.")
    return redirect("Recever_requestsDoctor")


def assign_surgery(request, pk):
    try:
        organ_request = Organrequest.objects.get(id=pk)
        # Logic to assign surgery can be added here
        if request.method == "POST":
            admit_date = request.POST.get("admit_date")
            surgery_date = request.POST.get("surgery_date")
            comments_doctor = request.POST.get("comments_doctor")
            try:
                surgery = Surgery.objects.create(
                    organrequest=organ_request,
                    admint_date=admit_date,
                    surgery_date=surgery_date,
                    comments_doctor=comments_doctor,
                    patient=organ_request.patient,
                    donar=organ_request.Donar
                )
            except:
                messages.success(request, "Please add Donar To Request...")
                return redirect("view_receiver_request_doctor", pk= pk)
            surgery.save()
            messages.success(request, "Surgery assigned successfully.")
            return redirect("surgery_doctor")
       
    except Organrequest.DoesNotExist:
        messages.error(request, "Request not found.")
    return redirect("Recever_requestsDoctor")

def surgery_status_change(request, pk):
    try:
        surgery = Surgery.objects.get(id=pk)
        surgery.completion_status = True
        surgery.surgery_status = True
        surgery.save()
        messages.success(request, "Surgery status updated successfully.")
        return redirect(reverse("surgery_doctor"))

    except Surgery.DoesNotExist:
        messages.error(request, "Surgery not found.")
    return redirect(reverse("surgery_doctor"))
   

def surgery_view_receiver(request):
    user = ReceiverProfile.objects.get(user = request.user)
    surgery = Surgery.objects.filter(patient = user)
    return render(request,"surgery_receiver.html",{"surgery":surgery})

def surgery_view_donar(request):
    user = UserProfile.objects.get(user = request.user)
    surgery = Surgery.objects.filter(donar = user)
    return render(request,"surgery_donar.html",{"surgery":surgery})

def surgery_doctor(request):
    user  = DoctorProfile.objects.get(user = request.user)
    surgery = Surgery.objects.filter(organrequest__doctor=user) 
    return render(request, 'doctorsurgery.html',{"surgery":surgery})

def Approve_donar_donation_requests(request, pk):
    try:
        donation_request = Organrequest.objects.get(id=pk)
        donation_request.Donar_approval = True
        donation_request.save()
        messages.success(request, "Donation request approved successfully.")
    except Organrequest.DoesNotExist:
        messages.error(request, "Donation request not found.")
    return redirect("OrganDonations")


def Surgery_add(request):
    pass