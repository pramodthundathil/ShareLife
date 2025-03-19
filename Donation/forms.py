from .models import Consutation, OrganDonation, Surgery, Organrequest
from django.forms import ModelForm , Select, Textarea, TextInput, ClearableFileInput
from datetime import date

today = date.today()


class ConsultaionAdd(ModelForm):
    class Meta:
        model = Consutation
        fields = ["doctor","date","time"]
        widgets = {
            "date":TextInput(attrs={"type":"date","min":today,"class":"form-control"}),
            "time":TextInput(attrs={"type":"time","class":"form-control"}),
            "doctor":Select(attrs={"class":"form-control"}),
            "hospitel":Select(attrs={"class":"form-control"})
        }


class AddOrganDonation(ModelForm):

    class Meta:
        model = OrganDonation
        fields = ["organ","HealthPath","Hospital"]

        widgets = {
            # "doner":Select(attrs={"class":"form-control"}),
            "organ":Select(attrs={"class":"form-control"}),
            # "Bloodgroup":Select(attrs={"class":"form-control", "id":"blood"}),
            "HealthPath":TextInput(attrs={"class":"form-control"}),            
            "Hospital":Select(attrs={"class":"form-control"}),
        }


class OrganDonationRequest(ModelForm):
    class Meta:
        model = Organrequest
        fields = ["organ","doctor","HealthRecord"]
        widgets = {
            "organ":Select(attrs={"class":"form-control"}),
            "doctor":Select(attrs={"class":"form-control"}),
            "patient":Select(attrs={"class":"form-control"}),
            "HealthRecord":ClearableFileInput(attrs={"class":"form-control","type":"file"})
        }

class SurgeyAdd(ModelForm):
    class Meta:
        model = Surgery
        fields = ["patient","surgery_date","donar","admint_date","comments_doctor"]

        widgets = {
            "surgery_date":TextInput(attrs={"class":"form-control","type":"date"}),
            "admint_date":TextInput(attrs={"class":"form-control","type":"date"}),
            "patient":Select(attrs={"class":"form-control"}),
            'donar':Select(attrs={"class":"form-control"}),
            "comments_doctor":TextInput(attrs={"class":"form-control"}),            
            
        }
