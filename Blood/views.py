from django.shortcuts import render, redirect, get_object_or_404
from .models import BloodDonation, BloodReceptRequests, BloodVault
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.



def donate_blood(request):
    donations = BloodDonation.objects.filter(user = request.user)
    blood_group = request.user.profile.Bloodgroup
    if request.method == "POST":
        unit = request.POST.get("unit")
        donation = BloodDonation.objects.create(user = request.user, donated_group = blood_group, unit = unit)
        donation.save()
        messages.success(request,"Donation request posted..")
        return redirect("donate_blood")
    return render(request,"donate-blood.html",{"donations":donations,"blood_group":blood_group})

def blood_receiver(request):
    requests = BloodDonation.objects.all()

    context = {
        "requests":requests
    }

    return render(request, "blood_receiver_requests.html",context)



@csrf_exempt
def approve_request(request, request_id):
    if request.method == "POST":
        donation_request = get_object_or_404(BloodDonation, id=request_id)
        if not donation_request.approval:
            donation_request.approval = True
            donation_request.save()

            blood_vault, created = BloodVault.objects.get_or_create(
                blood_group=donation_request.donated_group,
                defaults={"total_unit": 0}
            )
            blood_vault.total_unit += donation_request.unit
            blood_vault.save()

            messages.success(request, "Donation request approved and blood vault updated.")
            return redirect("BloodGroupsAdmin")

        else:
            messages.warning(request, "This request is already approved.")
        return redirect("BloodGroupsAdmin")
    return HttpResponse(status=405)  # Method Not Allowed


@csrf_exempt
def approve_receiver_request(request, request_id):
    if request.method == "POST":
        receiver_request = get_object_or_404(BloodReceptRequests, id=request_id)
        if not receiver_request.approval:
            blood_vault = BloodVault.objects.filter(blood_group=receiver_request.requested_group).first()
            if blood_vault and blood_vault.total_unit >= receiver_request.unit:
                blood_vault.total_unit -= receiver_request.unit
                blood_vault.save()

                receiver_request.approval = True
                receiver_request.save()

                messages.success(request, "Receiver request approved and blood vault updated.")
            else:
                messages.error(request, "Insufficient blood units available in the vault for the requested group.")
            return redirect("BloodGroupsAdmin")
        else:
            messages.warning(request, "This request is already approved.")
        return redirect("BloodGroupsAdmin")
    return HttpResponse(status=405)  # Method Not Allowed


def blood_donation_requests(request):
    requests = BloodReceptRequests.objects.all()
    return render(request,"blood_donation_requests.html",{"requests":requests})

def admin_blood(request):
    # total_blood_units = BloodVault.objects.aggregate(total_units=models.Sum('total_unit'))['total_units'] or 0
    pending_donation_requests = BloodDonation.objects.filter(approval=False).count()
    pending_receiver_requests = BloodReceptRequests.objects.filter(approval=False).count()

    context = {
        # "total_blood_units": total_blood_units,
        "pending_donation_requests": pending_donation_requests,
        "pending_receiver_requests": pending_receiver_requests,
    }


    return render(request,"blood_donation_admin.html",context)


def BloodGroupsAdmin(request):
    blood_vault = BloodVault.objects.all()
    if request.method == "POST":
        blood_group = request.POST.get("blood_group")
        total_unit = request.POST.get("total_unit")
        if BloodVault.objects.filter(blood_group=blood_group).exists():

            blood_vault = BloodVault.objects.get(blood_group=blood_group)
            blood_vault.total_unit += int(total_unit)
            blood_vault.save()
            messages.success(request, "Blood vault updated successfully.")
            return redirect("BloodGroupsAdmin")
        else:
            blood_vault = BloodVault.objects.create(blood_group=blood_group, total_unit=total_unit)
            blood_vault.save()
            messages.success(request, "Blood vault updated successfully.")
            return redirect("BloodGroupsAdmin")

    context = {
        "blood_vault":blood_vault
    }
    return render(request,"vault_admin.html",context)


def MyBloodDonationRequest(request):
    requests = BloodReceptRequests.objects.filter(user=request.user)

    if request.method == "POST":
        requested_group = request.POST.get("requested_group")
        unit = request.POST.get("unit")
        blood_request = BloodReceptRequests.objects.create(
            user=request.user,
            requested_group=requested_group,
            unit=unit
        )
        blood_request.save()
        messages.success(request, "Blood request submitted successfully.")
        return redirect("MyBloodDonationRequest")

    return render(request, "my_blood_requests.html", {"requests": requests})



    
    
  