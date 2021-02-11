#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:49:27 2020

@author: clairericks
"""

from warehouse_inventory import Inventory

import kivy

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView


class CustomBoxLayout(BoxLayout):
    pass


class CustomGridLayout(GridLayout):
    pass


class OpenScreen(Screen):
    access = ObjectProperty()
    name = StringProperty('')
    
    def __init__(self, **kwargs):
        super(OpenScreen, self).__init__(**kwargs)

    def get_text(self, *args):
        self.inventory = self.access.text.strip()
        self.open_inventory(self.inventory)
    
    def open_inventory(self, name):
        self.i = Inventory(name)


class RemovePopup(Popup):
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(RemovePopup, self).__init__(**kwargs)
        self.obj = obj


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
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
        popup = RemovePopup(self)
        popup.open()

    def remove_item(self):
        self.i = sm.get_screen('open').i
        self.i.remove_item(self.text)

    def update_changes(self):
        self.text = ''


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class List(Popup):
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    update = ListProperty([])

    def __init__(self, obj, **kwargs):
        super(List, self).__init__(**kwargs)
        self.obj = obj
        update = sm.get_screen('options').data_items
        self.ids.db.data = [{'text': str(x)} for x in update]


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)

    def get_data(self):
        self.data_items = []
        self.i = sm.get_screen('open').i
        rows = self.i.view_items('Locations')

        for row in rows:
            for col in row:
                self.data_items.append(col)

    def on_view(self):
        popup = List(self)
        popup.open()


class AddScreen(Screen):
    item = ObjectProperty()
    location = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
    
    def add_item_location(self, *args):
        self.i = sm.get_screen('open').i
        self.i.add_item(self.item.text.strip(), self.location.text.strip())


class AddAnotherScreen(Screen):
    pass


class ChangeLocScreen(Screen):
    item = ObjectProperty()
    location = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChangeLocScreen, self).__init__(**kwargs)

    def change_loc(self, *args):
        self.i = sm.get_screen('open').i
        self.i.update_location(self.item.text.strip(), self.location.text.strip())


class ChangeAnotherScreen(Screen):
    pass


class DeleteScreen(Screen):
    item = ObjectProperty()

    def __init__(self, **kwargs):
        super(DeleteScreen, self).__init__(**kwargs)

    def delete_item(self, *args):
        self.i = sm.get_screen('open').i
        self.i.remove_item(self.item.text.strip())


Builder.load_file('screens.kv')


sm = ScreenManager()
sm.add_widget(OpenScreen())
sm.add_widget(OptionsScreen())
sm.add_widget(AddScreen())
sm.add_widget(AddAnotherScreen())
sm.add_widget(ChangeLocScreen())
sm.add_widget(ChangeAnotherScreen())
sm.add_widget(DeleteScreen())

class MainApp(App):
    def build(self):
        return sm


kv = MainApp()
kv.run()
    
