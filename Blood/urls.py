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
]