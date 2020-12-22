"""
Created on Mon Nov 16 18:20:17 2020

@author: clairericks
"""
###############################################################################
# Scrapes Rocky Mountain Flora website to add all plants to SQLite Database.  # 
# Had to use two rounds to gather plants, because website was not organized   #
# uniformly.                                                                  #
###############################################################################


import re
import requests
import sqlite3
from bs4 import BeautifulSoup
from collections import namedtuple

from time import sleep
from random import randint

def getPlants():
    URL = 'https://www.rockymountainsflora.com/colors/family_list1.htm'
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
    table = soup.find('table')


    file = open('plants_two.txt', 'w')
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        for td in cells:
            if not td.text.strip(): continue
            file.write(td.text + '\n')
    file.close()


def plantTable():
    file = open('plants_two.txt', 'r')
    Table_Element = namedtuple('Plant',
                            ['latin', 'name', 'color', 'zones', 'habitat'])
    plants = {}
    singlePlant = []
    for line in file:
        line = line.strip()
        if line.startswith('Family'):
            family = line[8:]
            plants.setdefault(family, [])
            continue
        singlePlant.append(line)
        if len(singlePlant) == 5:
            plants[family].append(Table_Element(singlePlant[0], singlePlant[1],
                                                singlePlant[2], singlePlant[3],
                                                singlePlant[4]))
            singlePlant = []
    return plants


def makePlantDatabase():
    conn = sqlite3.connect('SanJuanPlants.sqlite')
    cur = conn.cursor()
    cur.executescript('''CREATE TABLE Colors
                      (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      name TEXT UNIQUE);
                      
                      CREATE TABLE Zones
                      (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      name TEXT UNIQUE);
                      
                      CREATE TABLE Habitat
                      (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      name TEXT UNIQUE);
                      
                      CREATE TABLE Plant
                      (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      latin TEXT UNIQUE,
                      name TEXT UNIQUE,
                      color_id INTEGER,
                      zones_id INTEGER,
                      habitat_id INTEGER,
                      details TEXT);
                      
                      CREATE TABLE Family
                      (name TEXT UNIQUE,
                       plant_id INTEGER);''')

    plants = plantTable()
    for family in plants:
        for plant in plants[family]:
            cur.execute('''INSERT OR IGNORE INTO Colors (name)
                        VALUES (?)''', (plant.color,))
            cur.execute('SELECT id FROM Colors WHERE name = ?', (plant.color,))
            color_id = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO Zones (name)
                        VALUES (?)''', (plant.zones,))
            cur.execute('SELECT id FROM Zones WHERE name = ?', (plant.zones,))
            zones_id = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO Habitat (name)
                        VALUES (?)''', (plant.habitat,))
            cur.execute('SELECT id FROM Habitat WHERE name = ?', (plant.habitat,))
            habitat_id = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO Plant (name, latin, color_id,
                        zones_id, habitat_id) VALUES (?, ?, ?, ?, ?)''', 
                        (plant.name, plant.latin, color_id, zones_id, habitat_id))
            cur.execute('SELECT id FROM Plant WHERE name = ?', (plant.name,))
            plant_id = cur.fetchone()[0]
            cur.execute('''INSERT OR IGNORE INTO Family (name, plant_id)
                        VALUES (?, ?)''', (family, plant_id))
            conn.commit()

       
            
def getLinks():
    URL = 'https://www.rockymountainsflora.com/colors/family_list1.htm'
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
    table = soup.find('table')
    links = table.find_all('a')
    file = open('plant_links.txt', 'w')
    for link in links:
        file.write(link.get('href') + '\n')
    file.close()
    

def addText():
    file = open('plant_links.txt', 'r')
    conn = sqlite3.connect('SanJuanPlants.sqlite')
    cur = conn.cursor()
    for link in file:
        link = link.strip()
        if link == 'None': continue
    
        URL = 'https://www.rockymountainsflora.com/' + link
        soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
        
        trs = soup.find_all('tr')
        for tr in trs:
            try:
                name = tr.span.text
                details = tr.find('p', class_='text').text
                cur.execute('''UPDATE Plant SET details = ? WHERE name = ?''',
                        (details, name))
                conn.commit()
            except:
                continue
        sleep(randint(2,10))

def getMissed():
    conn = sqlite3.connect('SanJuanPlants.sqlite')
    cur = conn.cursor()
    entries = cur.execute('''SELECT latin FROM Plant WHERE details IS NULL''').fetchall()
    entries = [entry[0] for entry in entries]
    file = open('plant_links_missed.txt', 'w')

    URL = 'https://www.rockymountainsflora.com/colors/family_list1.htm'
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        try:
            if not row.td.text.strip(): continue
            if row.td.text.strip() in entries:
                file.write(row.td.text.strip() + '  ' + row.a.get('href') + '\n')
        except:
            continue
    file.close()


def addTextToMissed():
    file = open('plant_links_missed.txt', 'r')
    conn = sqlite3.connect('SanJuanPlants.sqlite')
    cur = conn.cursor()
    for line in file:
        result = line.split('  ')
        latin = result[0]
        link = result[1]
        print(latin)

        URL = 'https://www.rockymountainsflora.com/' + link
        soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
        
        trs = soup.find_all('tr')
        for tr in trs:
            try:
                details = tr.find('p', class_='text').text
                cur.execute('''UPDATE Plant SET details = ? WHERE latin = ?''',
                        (details, latin))
                conn.commit()
            except:
                continue
        sleep(randint(2,10))
