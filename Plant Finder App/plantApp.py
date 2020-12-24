#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:12:27 2020

@author: clairericks
"""

import sqlite3

import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class FindOptions(Screen): 
    
    def openPlantDB(self): 
        conn = sqlite3.connect('SanJuanPlants.sqlite')
        cur = conn.cursor() 
    
class PlantScreen(Screen):
    plantDB = ObjectProperty()
    
    def accessPlant(self, *args): 
         
    
