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




def reports_admin(request):
    blood_vault = BloodVault.objects.all()
    total_blood_units = sum(vault.total_unit for vault in blood_vault)
    context = {
        "blood_vault": blood_vault,
        "total_blood_units": total_blood_units,
    }
    return render(request, "reports_admin.html", context)  
    
  
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from .models import BloodVault, BloodReceptRequests, BloodDonation
from django.contrib.auth.decorators import login_required

def generate_blood_vault_report(request):
    """
    Generate an Excel report for all blood inventory in the vault
    """
    # Get all blood vault records
    blood_inventory = BloodVault.objects.all()
    
    # Create a dataframe with the blood inventory data
    data = {
        'Blood Group': [inventory.blood_group for inventory in blood_inventory],
        'Total Units': [inventory.total_unit for inventory in blood_inventory],
        'Last Updated': [inventory.updated_on for inventory in blood_inventory],
    }
    
    df = pd.DataFrame(data)
    
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=blood_inventory_report_{timestamp}.xlsx'
    
    # Write the dataframe to Excel
    df.to_excel(response, index=False, sheet_name='Blood Inventory')
    
    return response

@login_required
def generate_blood_request_report(request, start_date=None, end_date=None, approved_only=False):
    """
    Generate an Excel report for blood requests with optional filtering
    """
    # Start with all requests
    blood_requests = BloodReceptRequests.objects.all()
    
    # Apply filters if provided
    if start_date:
        blood_requests = blood_requests.filter(date__gte=start_date)
    
    if end_date:
        blood_requests = blood_requests.filter(date__lte=end_date)
    
    if approved_only:
        blood_requests = blood_requests.filter(approval=True)
    
    # Create a dataframe with the blood requests data
    data = {
        'Requester': [request.user.username for request in blood_requests],
        'Blood Group': [request.requested_group for request in blood_requests],
        'Units': [request.unit for request in blood_requests],
        'Request Date': [request.date for request in blood_requests],
        'Last Updated': [request.updated_date for request in blood_requests],
        'Approved': [request.approval for request in blood_requests],
    }
    
    df = pd.DataFrame(data)
    
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filter_info = "_filtered" if (start_date or end_date or approved_only) else ""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=blood_requests_report{filter_info}_{timestamp}.xlsx'
    
    # Write the dataframe to Excel
    df.to_excel(response, index=False, sheet_name='Blood Requests')
    
    return response

@login_required
def generate_blood_donation_report(request, start_date=None, end_date=None, approved_only=False):
    """
    Generate an Excel report for blood donations with optional filtering
    """
    # Start with all donations
    blood_donations = BloodDonation.objects.all()
    
    # Apply filters if provided
    if start_date:
        blood_donations = blood_donations.filter(donated_date__gte=start_date)
    
    if end_date:
        blood_donations = blood_donations.filter(donated_date__lte=end_date)
    
    if approved_only:
        blood_donations = blood_donations.filter(approval=True)
    
    # Create a dataframe with the blood donations data
    data = {
        'Donor': [donation.user.username for donation in blood_donations],
        'Blood Group': [donation.donated_group for donation in blood_donations],
        'Units': [donation.unit for donation in blood_donations],
        'Donation Date': [donation.donated_date for donation in blood_donations],
        'Approved': [donation.approval for donation in blood_donations],
    }
    
    df = pd.DataFrame(data)
    
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filter_info = "_filtered" if (start_date or end_date or approved_only) else ""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=blood_donations_report{filter_info}_{timestamp}.xlsx'
    
    # Write the dataframe to Excel
    df.to_excel(response, index=False, sheet_name='Blood Donations')
    
    return response

def generate_comprehensive_blood_report(request):
    """
    Generate a comprehensive Excel report with multiple sheets for inventory, requests, and donations
    """
    # Create an Excel writer object
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=comprehensive_blood_report_{timestamp}.xlsx'
    
    # Create the excel file
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    
    # Generate inventory data
    blood_inventory = BloodVault.objects.all()
    inventory_data = {
        'Blood Group': [inventory.blood_group for inventory in blood_inventory],
        'Total Units': [inventory.total_unit for inventory in blood_inventory],
        'Last Updated': [inventory.updated_on for inventory in blood_inventory],
    }
    inventory_df = pd.DataFrame(inventory_data)
    
    # Generate requests data
    blood_requests = BloodReceptRequests.objects.all()
    requests_data = {
        'Requester': [req.user.username for req in blood_requests],
        'Blood Group': [req.requested_group for req in blood_requests],
        'Units': [req.unit for req in blood_requests],
        'Request Date': [req.date for req in blood_requests],
        'Last Updated': [req.updated_date for req in blood_requests],
        'Approved': [req.approval for req in blood_requests],
    }
    requests_df = pd.DataFrame(requests_data)
    
    # Generate donations data
    blood_donations = BloodDonation.objects.all()
    donations_data = {
        'Donor': [donation.user.username for donation in blood_donations],
        'Blood Group': [donation.donated_group for donation in blood_donations],
        'Units': [donation.unit for donation in blood_donations],
        'Donation Date': [donation.donated_date for donation in blood_donations],
        'Approved': [donation.approval for donation in blood_donations],
    }
    donations_df = pd.DataFrame(donations_data)
    
    # Write each dataframe to a different sheet
    inventory_df.to_excel(writer, sheet_name='Blood Inventory', index=False)
    requests_df.to_excel(writer, sheet_name='Blood Requests', index=False)
    donations_df.to_excel(writer, sheet_name='Blood Donations', index=False)
    
    # Apply some formatting with xlsxwriter
    workbook = writer.book
    
    # Format for headers
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Apply the header format to each sheet
    for sheet_name in ['Blood Inventory', 'Blood Requests', 'Blood Donations']:
        worksheet = writer.sheets[sheet_name]
        for col_num, value in enumerate(writer.sheets[sheet_name].get_row_data(0)):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)  # Set column width
    
    # Add a summary sheet
    summary_data = {
        'Category': ['Total Blood Groups', 'Total Inventory Units', 'Total Requests', 'Approved Requests', 
                     'Total Donations', 'Approved Donations'],
        'Count': [
            BloodVault.objects.values('blood_group').distinct().count(),
            sum(inventory.total_unit for inventory in blood_inventory),
            blood_requests.count(),
            blood_requests.filter(approval=True).count(),
            blood_donations.count(),
            blood_donations.filter(approval=True).count()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Apply formatting to summary sheet
    summary_sheet = writer.sheets['Summary']
    for col_num, value in enumerate(summary_df.columns):
        summary_sheet.write(0, col_num, value, header_format)
        summary_sheet.set_column(col_num, col_num, 20)
    
    # Save the workbook
    writer.close()
    
    return response



import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from Donation.models import OrganDonation, Organrequest, Surgery
from django.contrib.auth.decorators import login_required

@login_required
def generate_organ_donation_report(request, available_only=False):
    """
    Generate an Excel report for organ donations with optional filtering
    """
    # Start with all organ donations
    organ_donations = OrganDonation.objects.all()
    
    # Apply filter if requested
    if available_only:
        organ_donations = organ_donations.filter(availability=True)
    
    # Create a dataframe with the organ donations data
    data = {
        'Donor': [donation.doner.user.username if donation.doner else "N/A" for donation in organ_donations],
        'Organ Type': [donation.organ for donation in organ_donations],
        'Blood Group': [donation.Bloodgroup for donation in organ_donations],
        'Health Path': [donation.HealthPath for donation in organ_donations],
        'Hospital': [donation.Hospital.name if donation.Hospital else "N/A" for donation in organ_donations],
        'Available': [donation.availability for donation in organ_donations],
    }
    
    df = pd.DataFrame(data)
    
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filter_info = "_available_only" if available_only else ""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=organ_donations_report{filter_info}_{timestamp}.xlsx'
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    
    # Write the dataframe to Excel
    df.to_excel(writer, index=False, sheet_name='Organ Donations')
    
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Organ Donations']
    
    # Add header format
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Apply the header format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 15)  # Set column width
    
    # Set health path column to be wider
    worksheet.set_column(3, 3, 40)  # Health path column
    
    # Close the Pandas Excel writer and output the Excel file
    writer.close()
    
    return response

@login_required
def generate_organ_request_report(request, status=None, start_date=None, end_date=None):
    """
    Generate an Excel report for organ requests with optional filtering
    """
    # Start with all organ requests
    organ_requests = Organrequest.objects.all()
    
    # Apply filters if provided
    if status:
        organ_requests = organ_requests.filter(status=status)
    
    if start_date:
        organ_requests = organ_requests.filter(date__gte=start_date)
    
    if end_date:
        organ_requests = organ_requests.filter(date__lte=end_date)
    
    # Create a dataframe with the organ requests data
    data = {
        'Organ Type': [request.organ for request in organ_requests],
        'Blood Group': [request.Bloodgroup for request in organ_requests],
        'Doctor': [request.doctor.user.username if request.doctor else "N/A" for request in organ_requests],
        'Patient': [request.patient.user.username if request.patient else "N/A" for request in organ_requests],
        'Donor': [request.Donar.user.username if request.Donar else "Not Assigned" for request in organ_requests],
        'Donor Approval': [request.Donar_approval for request in organ_requests],
        'Request Active': [request.request_status for request in organ_requests],
        'Health Record Status': [request.is_healthrecord_status for request in organ_requests],
        'Approval Status': [request.approval_status for request in organ_requests],
        'Status': [request.status for request in organ_requests],
        'Request Date': [request.date for request in organ_requests],
    }
    
    df = pd.DataFrame(data)
    
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filter_info = f"_{status}" if status else ""
    filter_info += "_filtered" if (start_date or end_date) else ""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=organ_requests_report{filter_info}_{timestamp}.xlsx'
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    
    # Write the dataframe to Excel
    df.to_excel(writer, index=False, sheet_name='Organ Requests')
    
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Organ Requests']
    
    # Add header format
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Apply the header format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 15)  # Set column width
    
    # Close the Pandas Excel writer and output the Excel file
    writer.close()
    
    return response

@login_required
def generate_surgery_report(request, completed_only=False, start_date=None, end_date=None):
    """
    Generate an Excel report for surgeries with optional filtering
    """
    # Start with all surgeries
    surgeries = Surgery.objects.all()
    
    # Apply filters if provided
    if completed_only:
        surgeries = surgeries.filter(completion_status=True)
    
    if start_date:
        surgeries = surgeries.filter(surgery_date__gte=start_date)
    
    if end_date:
        surgeries = surgeries.filter(surgery_date__lte=end_date)
    
    # Create a dataframe with the surgeries data
    data = {
        'Patient': [surgery.patient.user.username if surgery.patient else "N/A" for surgery in surgeries],
        'Donor': [surgery.donar.user.username if surgery.donar else "N/A" for surgery in surgeries],
        'Organ Request': [surgery.organrequest.organ if surgery.organrequest else "N/A" for surgery in surgeries],
        'Surgery Date': [surgery.surgery_date for surgery in surgeries],
        'Admission Date': [surgery.admint_date for surgery in surgeries],
        'Surgery Status': [surgery.surgery_status for surgery in surgeries],
        'Doctor Comments': [surgery.comments_doctor if surgery.comments_doctor else "" for surgery in surgeries],
        'Completed': [surgery.completion_status for surgery in surgeries],
    }
    
    df = pd.DataFrame(data)
    
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filter_info = "_completed_only" if completed_only else ""
    filter_info += "_dated" if (start_date or end_date) else ""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=surgeries_report{filter_info}_{timestamp}.xlsx'
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    
    # Write the dataframe to Excel
    df.to_excel(writer, index=False, sheet_name='Surgeries')
    
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Surgeries']
    
    # Add header format
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Apply the header format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 15)  # Set column width
    
    # Set doctor comments column to be wider
    worksheet.set_column(6, 6, 40)  # Doctor comments column
    
    # Close the Pandas Excel writer and output the Excel file
    writer.close()
    
    return response

def generate_comprehensive_organ_report(request):
    """
    Generate a comprehensive Excel report with multiple sheets for organ donations, requests, and surgeries
    """
    # Create a response object with Excel content
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=comprehensive_organ_report_{timestamp}.xlsx'
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    
    # Get the data for each model
    # Organ Donations
    organ_donations = OrganDonation.objects.all()
    donations_data = {
        'Donor': [donation.doner.user.username if donation.doner else "N/A" for donation in organ_donations],
        'Organ Type': [donation.organ for donation in organ_donations],
        'Blood Group': [donation.Bloodgroup for donation in organ_donations],
        'Health Path': [donation.HealthPath for donation in organ_donations],
        'Hospital': [donation.Hospital.name if donation.Hospital else "N/A" for donation in organ_donations],
        'Available': [donation.availability for donation in organ_donations],
    }
    donations_df = pd.DataFrame(donations_data)
    
    # Organ Requests
    organ_requests = Organrequest.objects.all()
    requests_data = {
        'Organ Type': [request.organ for request in organ_requests],
        'Blood Group': [request.Bloodgroup for request in organ_requests],
        'Doctor': [request.doctor.user.username if request.doctor else "N/A" for request in organ_requests],
        'Patient': [request.patient.user.username if request.patient else "N/A" for request in organ_requests],
        'Donor': [request.Donar.user.username if request.Donar else "Not Assigned" for request in organ_requests],
        'Donor Approval': [request.Donar_approval for request in organ_requests],
        'Request Active': [request.request_status for request in organ_requests],
        'Status': [request.status for request in organ_requests],
        'Request Date': [request.date for request in organ_requests],
    }
    requests_df = pd.DataFrame(requests_data)
    
    # Surgeries
    surgeries = Surgery.objects.all()
    surgeries_data = {
        'Patient': [surgery.patient.user.username if surgery.patient else "N/A" for surgery in surgeries],
        'Donor': [surgery.donar.user.username if surgery.donar else "N/A" for surgery in surgeries],
        'Organ Request': [surgery.organrequest.organ if surgery.organrequest else "N/A" for surgery in surgeries],
        'Surgery Date': [surgery.surgery_date for surgery in surgeries],
        'Admission Date': [surgery.admint_date for surgery in surgeries],
        'Surgery Status': [surgery.surgery_status for surgery in surgeries],
        'Completed': [surgery.completion_status for surgery in surgeries],
    }
    surgeries_df = pd.DataFrame(surgeries_data)
    
    # Write each dataframe to a different sheet
    donations_df.to_excel(writer, sheet_name='Organ Donations', index=False)
    requests_df.to_excel(writer, sheet_name='Organ Requests', index=False)
    surgeries_df.to_excel(writer, sheet_name='Surgeries', index=False)
    
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    
    # Add header format
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Apply the header format to each sheet
    for sheet_name in ['Organ Donations', 'Organ Requests', 'Surgeries']:
        worksheet = writer.sheets[sheet_name]
        for col_num, value in enumerate(writer.sheets[sheet_name].get_row_data(0)):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)  # Set column width
    
    # Adjust specific columns
    writer.sheets['Organ Donations'].set_column(3, 3, 40)  # Health path column
    
    # Add a summary sheet
    summary_data = {
        'Category': ['Total Organ Donations', 'Available Organ Donations', 
                     'Total Organ Requests', 'Pending Requests', 'Approved Requests', 'Rejected Requests',
                     'Total Surgeries', 'Completed Surgeries', 'Scheduled Surgeries'],
        'Count': [
            organ_donations.count(),
            organ_donations.filter(availability=True).count(),
            organ_requests.count(),
            organ_requests.filter(status='Pending').count(),
            organ_requests.filter(status='Approved').count(),
            organ_requests.filter(status='Rejected').count(),
            surgeries.count(),
            surgeries.filter(completion_status=True).count(),
            surgeries.filter(surgery_status=True, completion_status=False).count()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Apply formatting to summary sheet
    summary_sheet = writer.sheets['Summary']
    for col_num, value in enumerate(summary_df.columns):
        summary_sheet.write(0, col_num, value, header_format)
        summary_sheet.set_column(col_num, col_num, 20)
    
    # Add organ type distribution chart
    organ_counts = {}
    for donation in organ_donations:
        organ_type = donation.organ
        if organ_type in organ_counts:
            organ_counts[organ_type] += 1
        else:
            organ_counts[organ_type] = 1
    
    organ_dist_data = {
        'Organ Type': list(organ_counts.keys()),
        'Count': list(organ_counts.values())
    }
    organ_dist_df = pd.DataFrame(organ_dist_data)
    organ_dist_df.to_excel(writer, sheet_name='Organ Distribution', index=False)
    
    # Format organ distribution sheet
    organ_dist_sheet = writer.sheets['Organ Distribution']
    for col_num, value in enumerate(organ_dist_df.columns):
        organ_dist_sheet.write(0, col_num, value, header_format)
        organ_dist_sheet.set_column(col_num, col_num, 15)
    
    # Create a chart
    chart = workbook.add_chart({'type': 'column'})
    
    # Add a series to the chart
    chart.add_series({
        'name':       '=Organ Distribution!$B$1',
        'categories': '=Organ Distribution!$A$2:$A$' + str(len(organ_counts) + 1),
        'values':     '=Organ Distribution!$B$2:$B$' + str(len(organ_counts) + 1),
    })
    
    # Configure the chart
    chart.set_title({'name': 'Organ Donations by Type'})
    chart.set_x_axis({'name': 'Organ Type'})
    chart.set_y_axis({'name': 'Count'})
    
    # Insert the chart into the worksheet
    organ_dist_sheet.insert_chart('D2', chart, {'x_scale': 1.5, 'y_scale': 1})
    
    # Close the Pandas Excel writer and output the Excel file
    writer.close()
    
    return response

