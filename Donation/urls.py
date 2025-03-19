from django.urls import path 
from .import views

urlpatterns = [
    path("GetAppoinment",views.GetAppoinment,name="GetAppoinment"),
    path("MyAppointments",views.MyAppointments,name="MyAppointments"),
    path("Doctors",views.Doctors,name="Doctors"),
    path("OrganDonations",views.OrganDonations,name="OrganDonations"),
    path("Surgeryview",views.Surgeryview,name="Surgeryview"),
    path("DoctorConsultaion",views.DoctorConsultaion,name="DoctorConsultaion"),
    path("DoctorSurgery",views.DoctorSurgery,name="DoctorSurgery"),
    path("OrganDonationAdd",views.OrganDonationAdd,name="OrganDonationAdd"),
    path("DoctordonationView",views.DoctordonationView,name="DoctordonationView"),
    path("DoctordonationView_approved",views.DoctordonationView_approved,name="DoctordonationView_approved"),
    
    path("ApproveConsultationrequest/<int:pk>",views.ApproveConsultationrequest,name="ApproveConsultationrequest"),
    path("AddOrganRequets",views.AddOrganRequets,name="AddOrganRequets"),
    path("ConsultationrequestsHospitels",views.ConsultationrequestsHospitels,name="ConsultationrequestsHospitels"),
    path("Addsurgery/<int:pk>",views.Addsurgery,name="Addsurgery"),
    path("SurgeryHospital",views.SurgeryHospital,name="SurgeryHospital"),
    path("OrganDonationHospital",views.OrganDonationHospital,name="OrganDonationHospital"),
    path('getbloodgroup/<int:donor_id>/', views.getbloodgroup, name='getbloodgroup'),
    path("UploadRecord/<int:pk>",views.UploadRecord,name="UploadRecord"),
    path("OrgandonationRequests",views.OrgandonationRequests,name="OrgandonationRequests"),
    path("Recever_requestsDoctor",views.Recever_requestsDoctor,name="Recever_requestsDoctor"),

    path("view_receiver_request_doctor/<int:pk>", views.view_receiver_request_doctor, name="view_receiver_request_doctor"),
    path("organ_approve/<int:pk>", views.organ_approve, name="organ_approve"),
    path("reject_request/<int:pk>", views.reject_request, name="reject_request"),
    path("assign_surgery/<int:pk>", views.assign_surgery, name="assign_surgery"),
    path("assign_donar/<int:pk>", views.assign_donar, name="assign_donar"),
    path("Approve_donar_donation_requests/<int:pk>", views.Approve_donar_donation_requests, name="Approve_donar_donation_requests"),

    path("surgery_doctor", views.surgery_doctor, name="surgery_doctor"),
    path("surgery_view_receiver", views.surgery_view_receiver, name="surgery_view_receiver"),
    path("surgery_view_donar", views.surgery_view_donar, name="surgery_view_donar"),
    path("surgery_status_change/<int:pk>",views.surgery_status_change,name="surgery_status_change")

    
]       
  
