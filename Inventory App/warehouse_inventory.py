#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:27:49 2020

@author: clairericks
"""

import sqlite3


class Inventory(object): 
    '''Inventory information'''
    def __init__(self, name):
        '''Opens sqlite and calls create_database method
            '''
        self.name = name.lower()
        self.openDB()
        self.create_database()
        
    def create_database(self):
        self.cur.executescript('''CREATE TABLE IF NOT EXISTS Locations
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                 name TEXT UNIQUE);
                                  
                CREATE TABLE IF NOT EXISTS Items
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                 name TEXT UNIQUE);
                
                CREATE TABLE IF NOT EXISTS Inventory
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                 items_id INTEGER,
                 locations_id INTEGER)''')
        self.executeClose()
    
    def executeClose(self): 
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def openDB(self):
        self.conn = sqlite3.connect('{}.sqlite'.format(self.name))
        self.cur = self.conn.cursor()
        return self.cur
    
    def addItem(self, name, location): 
        '''
        Enters name and location of item into SQLite database and updates
        Items, Locations, and Inventory tables with corresponding ids. 
        
        If the item is already in the Items table, returns 
        "Item already entered in system."
        '''
        name = name.lower()
        location = location.lower()
        self.openDB()
        self.cur.execute('SELECT count(*) FROM Items WHERE name = ?', (name,))
        item = self.cur.fetchone()[0]
        if item > 0: 
            return 'Item already entered in system.'
        try:
            self.cur.execute('''INSERT OR IGNORE INTO Locations (name) 
                             VALUES (?)''', (location,))
            self.cur.execute('SELECT id FROM Locations WHERE name = ?', (location,))
            locations_id = self.cur.fetchone()[0]
            
            self.cur.execute('''INSERT OR IGNORE INTO Items (name)
                             VALUES (?)''', (name,))
            self.cur.execute('SELECT id FROM Items WHERE name = ?', (name,))
            items_id = self.cur.fetchone()[0]
            
            self.cur.execute('''INSERT OR IGNORE INTO Inventory (items_id, locations_id) 
                             VALUES (?, ?)''', (items_id, locations_id))
            self.executeClose()
            return '{} located in {} entered into system'.format(name, location)
        except: 
            self.executeClose()
            return 'Something went wrong. Try again.'

    
    def updateLocation(self, name, location): 
        ''' 
        Updates location of item and inserts it into Locations table if not
        already there. Updates Inventory table with new location of item.
        
        If item is not in Items table, returns "Item not 
        entered in system."
        '''
        name = name.lower()
        location = location.lower()
        self.openDB()
        
        try: 
            self.cur.execute('SELECT id FROM Items WHERE name = ?', (name,))
            items_id = self.cur.fetchone()[0]
        except: 
            return 'Item not entered in system'
        
        self.cur.execute('''INSERT OR IGNORE INTO Locations (name) 
                         VALUES (?)''', (location,))
        self.cur.execute('SELECT id FROM Locations WHERE name = ?', (location,))
        locations_id = self.cur.fetchone()[0]
        
        self.cur.execute('''UPDATE Inventory SET locations_id = ? WHERE items_id = ?''',
                        (locations_id, items_id))

        self.executeClose()
        return '{} updated to new location: {}'.format(name, location)

    def removeItem(self, item):
        '''
        Removes specified item from database
        '''
        item = item.lower()
        self.openDB()

        self.cur.execute('DELETE FROM Items WHERE name = ?', (item,))
        self.executeClose()


    def viewItems(self, order): 
        ''' 
        Lists items and locations from Inventory table based on args
        '''
        
        
        self.openDB()
        self.cur.execute('''SELECT Items.name, Locations.name
                         FROM Inventory JOIN Items JOIN Locations ON 
                         Items.id = Inventory.items_id AND 
                         Locations.id = Inventory.locations_id
                         ORDER BY (?)''', (order,))
        return self.cur.fetchall()
        
    




            
            

   