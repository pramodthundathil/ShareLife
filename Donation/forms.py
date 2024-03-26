from .models import Consutation, OrganDonation, Surgery, Organrequest
from django.forms import ModelForm , Select, Textarea, TextInput
from datetime import date

today = date.today()


class ConsultaionAdd(ModelForm):
    class Meta:
        model = Consutation
        fields = ["doctor","hospitel","date","time"]
        widgets = {
            "date":TextInput(attrs={"type":"date","min":today,"class":"form-control"}),
            "time":TextInput(attrs={"type":"time","class":"form-control"}),
            "doctor":Select(attrs={"class":"form-control"}),
            "hospitel":Select(attrs={"class":"form-control"})
        }


class AddOrganDonation(ModelForm):
    class Meta:
        model = OrganDonation
        fields = ["doner","organ","Bloodgroup","HealthPath","Hospital"]

        widgets = {
            "doner":Select(attrs={"class":"form-control"}),
            "organ":TextInput(attrs={"class":"form-control"}),
            "Bloodgroup":Select(attrs={"class":"form-control"}),
            "HealthPath":Textarea(attrs={"class":"form-control"}),            
            "Hospital":Select(attrs={"class":"form-control"}),
        }
