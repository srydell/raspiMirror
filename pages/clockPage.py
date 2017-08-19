# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import datetime

class ClockPage(BoxLayout):
    clock_label = ObjectProperty()

    # Checks the time and updates the label text
    def update(self):
        dt = datetime.datetime.now()
        # First row: hours.minutes
        formatting = self.setSz(" %H.%M", 146)
        # First row: add smaller letters for seconds
        # and set a grey tone
        formatting += self.setClr(self.setSz("%S", 46), "#c7c5c5")
        # Second row: weekday, month dayOfMonth
        formatting += self.setSz("\n%a, %b %d", 65)
        clockString = dt.strftime(formatting)
        self.clock_label.markup = True
        self.clock_label.text = clockString

    # Repeates every clock cycle:
    # Checks the time and updates the label text
    def nextClockCycle(self, dt):
        self.update()

    def setSz(self, txt, size):
        return "[size={}]{}[/size]".format(size, txt)

    def setClr(self, txt, color):
        return "[color={}]{}[/color]".format(color, txt)
