from django.shortcuts import render
import json
import csv
import requests
from datetime import date
from urllib.request import urlopen
from django.core.mail import send_mail
from covidStatistics.models import CovidStatistics
from django.http import HttpResponseRedirect

# Create your views here.

api_url_base = ' https://covid19-api.weedmark.systems/api/v1/stats'
covidDataset = None

def index(request):

    country =''
    if  request.method == 'POST':
        country = request.POST.get('countryName')
    else:
        country = 'US'
    
    parameters = {
        "country": country
    }

    response = requests.get(api_url_base,  params=parameters)

    if response.status_code == 200:
        covidResult =  json.loads(response.content.decode('utf-8'))
        confirmed = 0
        deaths = 0 
        recovered = 0

        if len(covidResult['data']['covid19Stats']) > 1:      
            for x in covidResult['data']['covid19Stats']:
                confirmed += x['confirmed'] if x['confirmed'] != None  else 0
                deaths += x['deaths'] if  x['deaths'] != None  else 0
                recovered +=  x['recovered'] if  x['recovered'] != None else 0
        else:
            confirmed = int(covidResult['data']['covid19Stats'][0]['confirmed'])
            deaths = int(covidResult['data']['covid19Stats'][0]['deaths'])
            recovered = int(covidResult['data']['covid19Stats'][0]['recovered'])

        content = {
        'data' : covidResult['data']['covid19Stats'],
        'confirmed': confirmed,
        'deaths':  deaths,
        'recovered': recovered,
        'country': country,
        }  
        return render(request, 'index.html', {'contents': content})  

    else:
        return render(request, 'error.html') 


def dashboard(request):
    response = requests.get(api_url_base)
    dictPerCountry =  dict()
   
    message = None
    worldWideConfirmed =0
    worldWideDeaths = 0
    worldWideRecovered = 0
    if response.status_code == 200:
        covidResult =  json.loads(response.content.decode('utf-8'))

        for x in covidResult['data']['covid19Stats']:
            if x['country'] == "Cote d'Ivoire":
                # covidResult['data']['covid19Stats']['Cote d Ivoire'] = covidResult['data']['covid19Stats'].pop(x['country'])
                continue
                

            if(x['country']  not in dictPerCountry ):
                dictPerCountry[x['country']] =  CovidStatistics()
            
            confirmed = x['confirmed'] if x['confirmed'] != None  else 0
            deaths = x['deaths'] if  x['deaths'] != None  else 0
            recovered =  x['recovered'] if  x['recovered'] != None else 0

            # calculate the total wordl cases
            worldWideConfirmed +=  confirmed
            worldWideDeaths += deaths
            worldWideDeaths += worldWideRecovered

            # save in dictionary for each country the number of death toll, confirmed cases and recovered cases
            dictPerCountry[x['country']].setConfirmed(confirmed )
            dictPerCountry[x['country']].setDeaths( deaths)
            dictPerCountry[x['country']].setRecovered( recovered)

    else:
        message = response.status_code
    content = {
    'data' : dictPerCountry,
    'message': message if message != None else None,
    'confirmed': format(worldWideConfirmed, ',d'),
    'death' : format(worldWideDeaths,',d'),
    'recovered': format(worldWideRecovered,',d'),
    
    }  
    return render(request, 'dashboard.html', {'contents': content})  

def contact(request):
    return render(request, 'contact.html')  


def  email(request):
    if  request.method == 'POST':
        name =  request.POST.get('UserName')
        fromEmail =  request.POST.get('userEmail')
        toEmail = 'christellebinkal@gmail.com'
        subject =  request.POST.get('emailSubject')
        content =   ' Sender Name' + name + '\n'+ request.POST.get('emailBody')

        send_mail(subject,  content,fromEmail, list(toEmail), fail_silently=False )
    return HttpResponseRedirect('/contact/')