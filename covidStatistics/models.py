from django.db import models

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


