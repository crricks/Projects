#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 13:50:47 2020

@author: clairericks
"""
from bs4 import BeautifulSoup 
import urllib.request
import requests 
import re

from collections import namedtuple

class AvyReport(object): 
    
    def __init__(self): 
        self.data = []
        
    def openURL(self, page):
        URL = 'https://avalanche.state.co.us/' + page
        self.soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
        return self.soup
    
    def getArea(self): 
        soup = self.openURL('forecasts/backcountry-avalanche/north-san-juan/')
        self.area = soup.find('h1', class_='entry-title').text
        return self.area
    
    def getIframe(self, page):
        soup = self.openURL(page)
        self.iframe = soup.find('div', class_='entry-content').iframe
        return self.iframe['src']
    
    def getToday(self):
        soup = self.openURL(self.getIframe('forecasts/backcountry-avalanche/north-san-juan/'))
        text = soup.find('h2', class_='caption caption-controls').text.split()
        self.today = ' '.join(text[:7])
        self.name = ' '.join(text[7:])
        return self.today, self.name
    
    def getZones(self): 
        soup = self.openURL(self.getIframe('forecasts/backcountry-avalanche/north-san-juan/'))
        self.where = {}
        tbody = soup.tbody.find_all('td')
        for row in tbody: 
            if len(row.text.split()) == 2: 
                location = ' '.join(row.text.split())
            if location in self.where: 
                continue
            if len(row.text.split()) > 2: 
                self.where[location] = ' '.join(row.text.split())
        return self.where
                
    def getSummary(self):
        soup = self.openURL(self.getIframe('forecasts/backcountry-avalanche/north-san-juan/'))
        self.summary = soup.find('div', class_='span4 fx-text-area').text
        return self.summary
        
    def getStationData(self): 
        self.data = ['name', 'elev', 'Temp', 'MxTp', 'MnTp', 'DewP','RH', 'Spd', 'Dir', 
                'Gst', 'Pcp1', 'Pcp24','PcpAc', 'Sno24', 'SWE24', 'SnoHt', 'SWE']
        stations = ['Lizard Head Pass', 'PBasin Telluride Sk', 'Swamp Angel', 
                    'Red Mountain Pass', 'PHQ Telluride Ski R', 'Senator Beck', 
                    'Gold Hill Telluride']
        URL = 'https://avalanche.state.co.us/caic/obs_stns/zones.php'  
        source = urllib.request.urlopen(URL) 
        soup = BeautifulSoup(source, 'html.parser')  
        tds = soup.find_all('td')
        count = 17
        for td in tds: 
            if td.text in stations:
                area = td.text
                self.data.append(area)
                count = 0
                continue
            if count < 16: 
                self.data.append(td.text)
            count += 1
        return self.data
    
def createChart(): 
    report = ''
    nsj = AvyReport()
    area = nsj.getArea()
    today, name = nsj.getToday()
    report += '{}\n{}\n{}'.format(area, today, name)
    
    zoneInfo = nsj.getZones()
    above = zoneInfo['Above Treeline']
    near = zoneInfo['Near Treeline']
    below = zoneInfo['Below Treeline']
    report += '\n\nAbove Treeline: {}\nNear Treeline: {}\nBelow Treeline: {}'.format(above, near, below)
    
    summary = nsj.getSummary()
    report += '\n\n' + summary + '\n\n'
    
    data = nsj.getStationData()
    dataCopy = data[:]
  
    comp = []
    for i in range(17, 0, -1): 
        count = 0
        col = []
        for entry in dataCopy: 
            if count % i == 0: 
                col.append(entry)
            count += 1
        comp.append(col)
        for item in col: 
            dataCopy.remove(item)
    
    comp[0] = [col.rjust(19) for col in comp[0]]   
    comp[1] = [col.ljust(5) for col in comp[1]]
    for i in range(2, 11): 
        comp[i] = [col.center(4) for col in comp[i]]
    comp[6] = [col.ljust(3) for col in comp[6]]
    for i in range(11, 17):    
        comp[i] = [col.center(5) for col in comp[i]]
    
    
    for i in range(8): 
        together = ''
        for j in range(17):
            together += comp[j][i] + ' '
        report += '\n' + together
    
    return report 
