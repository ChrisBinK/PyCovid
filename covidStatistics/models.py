from django.db import models
from django import forms
# Create your models here.

class CovidStatistics:

    def __init__(self):
        self.confirmed = 0
        self.deaths = 0
        self.recovered = 0
    
    def setConfirmed(self, confirmed):
        self.confirmed += confirmed

    def getConfirmed(self):
        return format(self.confirmed, ',d')

    def setDeaths(self, deaths):
        self.deaths += deaths

    def getDeaths(self):
        return format(self.deaths, ',d')
    
    def setRecovered(self, recovered):
        self.recovered += recovered
    
    def getRecovered(self):
        return  format(self.recovered, ',d')


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    name =  forms.CharField()
    sender = forms.EmailField()
    recipients = forms.EmailField()
   

    def clean(self):
        cleaned_data = super().clean()
        self.subject = cleaned_data.get("emailSubject")
        self.sender = cleaned_data.get("userEmail")
        self.name = cleaned_data.get("UserName")
        self.message = cleaned_data.get("emailBody")
        return cleaned_data

