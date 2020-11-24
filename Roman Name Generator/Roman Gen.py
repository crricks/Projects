#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:06:09 2020

@author: clairericks
"""
import string
import random
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

Builder.load_string('''
<ScreenManagement>:
    MainScreen:
        id: main
        name: 'main'
    NameScreen:
        id: shown
        name: 'shown'
         
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas: 
            Color: 
                rgba: 255, 255, 255, 1
            Rectangle: 
                pos: self.pos
                size: self.size
        BoxLayout: 
            Image: 
                source: 'julius caesar.jpg'
                size_hint: 0.2, 1
            Label: 
                text: 'Join the Romans: A Name Generator'
                color: 1, 0, 0, 1
                bold: True
                italic: True
                font_size: 60
                halign: 'left'
        BoxLayout:
            Label:
                text: 'Enter your godforsaken plebe name.'
                color: 1, 0, 0, 1
            TextInput:
                id: txt_input
                text: ''
                font_size: 30
                halign: 'right'
                valign: 'center'
        BoxLayout:
            Button: 
                text: 'Quit'
                color: 1, 0, 0, 1
                background_color: 255, 255, 255, 1
                size_hint: 1, 0.5
                on_press: app.stop()
            Button:
                text: 'Enter'
                color: 1, 0, 0, 1
                background_color: 255, 255, 255, 1
                size_hint: 1, 0.5
                on_press: 
                    background_color = (1, 0, 0, 1)
                    root.manager.current = 'shown'
                on_release:
                    background_color = (255, 255, 255, 1)


<NameScreen>:
    roman: roman
    GridLayout:
        cols: 2
        canvas:
            Color:
                rgba: 255, 255, 255, 1
            Rectangle: 
                pos: self.pos
                size: self.size
        Image: 
            source: 'butt.jpg'
        Label:
            id: roman
            text: ''
            halign: 'left'
            color: 1, 0, 0, 1
            italic: True
            bold: True
            font_size: 60
        Button: 
            text: 'Convert Another'
            color: 1, 0, 0, 1
            background_color: 255, 255, 255, 1
            font_size: 30
            size_hint: 0.3, 0.5
            on_press: 
                root.manager.current = 'main'

                    ''')
                    
class MainScreen(Screen):
    pass

class NameScreen(Screen):
    def on_enter(self, *args):
        self.roman.text = self.roman_calculation(self.manager.ids.main.ids.txt_input.text)
        
    
    def roman_calculation(self, plebe):
        self.plebe = str(plebe).lower()
        response = ''
        if string.digits in self.plebe: 
            response = "Oh, you're very XXIst century.\n"
        full_name = self.plebe.split()
        self.roman_name = []
        for word in full_name: 
            added = ''
            if word[-1] in 'aeiouy':
                added = random.choice(['v', 'm', 'n', 'l', 'ns', 'rp'])
            roman_word = word + added + self.rom_ending()
            self.roman_name.append(roman_word.capitalize())
        self.roman_name = response + ' '.join(self.roman_name)
        return self.roman_name
    
    def rom_ending(self):
        roman_endings = open('latin_endings.txt', 'r')
        ending_list = []
        for word in roman_endings: 
            ending_list.append(word.strip())
        self.end = random.choice(ending_list)
        return self.end

class ScreenManagement(ScreenManager):
    pass

class testingApp(App):
    def build(self):
        return ScreenManagement()
    
if __name__ == '__main__':
    testingApp().run()

        
