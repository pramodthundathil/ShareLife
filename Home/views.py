from django.shortcuts import render, redirect
from .forms import UserAddForm, UserProfileAddForm, DoctorProfileAddForm, HospitalProfileAddForm
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_only, unautenticated_user, DoctorActiveCheck, HospitalActiveCheck
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import DoctorProfile, HospitalProfile, UserProfile, Block_1, Block_2, Block_3, Block_4

from .blockgenerator import Block
# Create your views here.

@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or Password Incorrect or You Are Not Activated")
            return redirect('SignIn')
    return render(request,"login.html")



@unautenticated_user
def SignUp(request):
    form = UserAddForm()
    form1 = UserProfileAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        form1 = UserProfileAddForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.save()
            user.save()
            userprofile = form1.save()
            userprofile.user = user
            userprofile.save()
            user.is_active = False
            user.save()

            # group = Group.objects.get(name='user')
            # user.groups.add(group) 
            # user.save()

            messages.info(request,"User Created Please Wait For Activation")
            return redirect('SignIn')
        else:
            messages.info(request,"Some thing wrong.....")
            return redirect('SignUp')

    return render(request,"register.html",{"form":form,"form1":form1})

@unautenticated_user
def DoctorSignUp(request):
    form = UserAddForm()
    form1 = DoctorProfileAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        form1 = DoctorProfileAddForm(request.POST,request.FILES)

        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()
            userprofile = form1.save()
            userprofile.user = user
            userprofile.save()

            group = Group.objects.get(name='doctor')
            user.groups.add(group) 
            user.save()
            
            # messages.info(request,"User Created")
            messages.info(request,"User Created Please Wait For Activation")

            return redirect('SignIn')
    return render(request,"doctorregister.html",{"form":form,"form1":form1})


def ValidateBlock(request,pk):
    medicine = UserProfile.objects.get(id = pk)
    block4 = Block_4.objects.get(MedicineBlock = medicine)
    block3 = Block_3.objects.get(MedicineBlock = medicine)
    block2 = Block_2.objects.get(MedicineBlock = medicine)
    block1 = block2.BlockLink
   
    BlockChanin2 = Block(3,medicine,block2.Blockhash)
    
    blockdata = [block1,block2,block3]
    blockhashvalue = Block(4,"time",blockdata,block3.Blockhash)
    print(blockhashvalue)
    
    if BlockChanin2.hash == block3.Blockhash:
        if blockhashvalue.hash == block4.Blockhash:
            messages.success(request,"This Donar is Valid")
            return redirect("ViewMed",pk=pk)            
        else:
            messages.info(request,"This Donar is InValid")
            return redirect("ViewMed",pk=pk)
    else:
        messages.info(request,"This Donar is InValid")
        return redirect("ViewMed",pk=pk)



from .forms import ReceiverProfileForm


@unautenticated_user
def ReceiverSignUp(request):
    form = UserAddForm()
    form1 = ReceiverProfileForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        form1 = ReceiverProfileForm(request.POST,request.FILES)

        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()
            userprofile = form1.save()
            userprofile.user = user
            userprofile.save()

            group = Group.objects.get(name='receiver')
            user.groups.add(group) 
            user.save()
            
            messages.info(request,"User Created")
            return redirect('SignIn')
    return render(request,"register_receiver.html",{"form":form,"form1":form1})


@unautenticated_user
def HospitalSignUp(request):
    form = UserAddForm()
    form1 = HospitalProfileAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        form1 = HospitalProfileAddForm(request.POST,request.FILES)

        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()
            userprofile = form1.save()
            userprofile.user = user
            userprofile.save()

            group = Group.objects.get(name='hospital')
            user.groups.add(group) 
            user.save()
            
            # messages.info(request,"User Created")
            messages.info(request,"User Created Please Wait For Activation")

            return redirect('SignIn')
    return render(request,"hospitalregister.html",{"form":form,"form1":form1})



def SignOut(request):
    logout(request)
    return redirect('SignIn')

def DonarApprove(request, pk):
    try:
        donar = User.objects.get(id=pk)
        donar.is_active = True
        donar.save()
        messages.info(request, "Donor Approved Successfully")
    except User.DoesNotExist:
        messages.error(request, "Donor not found")
    return redirect("DoctordonationView")


def DonarReject(request, pk):
    try:
        donar = User.objects.get(id=pk)
        donar.is_active = False
        donar.save()
        messages.info(request, "Donor Rejected Successfully")
    except UserProfile.DoesNotExist:
        messages.error(request, "Donor not found")
    return redirect("DoctordonationView")


def ApproveDoctor(request,pk):
    doctor = DoctorProfile.objects.get(id = pk)
    if doctor.active == False:
        doctor.active = True
        doctor.save()
    else:
        doctor.active = False
        doctor.save()

    messages.info(request, "Status Changed")
    return redirect("AdminIndex")

def ApproveHospital(request,pk):
    doctor = HospitalProfile.objects.get(id = pk)
    if doctor.active == False:
        doctor.active = True
        doctor.save()
    else:
        doctor.active = False
        doctor.save()
    messages.info(request, "Status Changed")
    return redirect("AdminIndex")



# indexpages and functionalities 


@admin_only
def Index(request):
    context = {

    }
    return render(request,"index.html",context)

@DoctorActiveCheck
def DoctorIndex(request):
    return render(request, "doctorindex.html")


@HospitalActiveCheck
def HospitalIndex(request):
    return render(request, "hospitalindex.html")

def AdminIndex(request):
    doctor = DoctorProfile.objects.all()
    hospital = HospitalProfile.objects.all()
    user = UserProfile.objects.all()

    context = {
        "doctor":doctor,
        "hospital":hospital,
        "user":user
    }
    return render(request, 'adminindex.html',context)


def ReceiverIndex(request):
    
    return render(request, "receiverindex.html")


