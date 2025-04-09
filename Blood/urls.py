from django.urls import path
from . import views

urlpatterns = [
    path('donate_blood/', views.donate_blood, name='donate_blood'),
    path('admin_blood/', views.admin_blood, name='admin_blood'),
    path("BloodGroupsAdmin",views.BloodGroupsAdmin,name="BloodGroupsAdmin"),
    path("blood_receiver",views.blood_receiver,name="blood_receiver"),
    path("approve_request/<int:request_id>",views.approve_request,name="approve_request"),
    path("approve_receiver_request/<int:request_id>",views.approve_receiver_request,name="approve_receiver_request"),
    path("MyBloodDonationRequest",views.MyBloodDonationRequest,name="MyBloodDonationRequest"),
    path("blood_donation_requests",views.blood_donation_requests,name="blood_donation_requests"),
    path("reports_admin",views.reports_admin,name="reports_admin"),

    path('reports/blood-inventory/', views.generate_blood_vault_report, name='blood_inventory_report'),
    path('reports/blood-requests/', views.generate_blood_request_report, name='blood_requests_report'),
    path('reports/blood-donations/', views.generate_blood_donation_report, name='blood_donations_report'),
    path('reports/comprehensive/', views.generate_comprehensive_blood_report, name='comprehensive_blood_report'),


    path('reports/organ-donations/', views.generate_organ_donation_report, name='organ_donations_report'),
    path('reports/organ-requests/', views.generate_organ_request_report, name='organ_requests_report'),
    path('reports/surgeries/', views.generate_surgery_report, name='surgeries_report'),
    path('reports/comprehensive-organ/', views.generate_comprehensive_organ_report, name='comprehensive_organ_report'),
]
