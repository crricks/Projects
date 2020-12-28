#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:12:27 2020

@author: clairericks
"""

import sqlite3

conn = sqlite3.connect('SanJuanPlants.sqlite')
cur = conn.cursor()

import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button


class FindOptions(Screen):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        pass


class RV(RecycleView):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class All(Screen):
    allPlants = ListProperty([])

    def __init__(self, **kwargs):
        super(All, self).__init__(**kwargs)
        self.getPlants()

    def getPlants(self, *args):
        cur.execute('SELECT name FROM Plant')
        self.allPlants = cur.fetchall()


class ColorButton(Button):
    pass


class Colors(Screen):
    pass


class PlantScreen(Screen):
    plantDB = ObjectProperty()
    
    def accessPlant(self, *args):
        pass


class ScreenManagement(ScreenManager):
    pass


Builder.load_file('plantScreens.kv')


class PlantApp(App):
    def build(self):
        sm = ScreenManagement()
        return sm


if __name__ == '__main__':
    PlantApp().run()

# First find by:
# Color
# Zone
# Name
# Family
# ScrollAll