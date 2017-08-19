# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from pages import rssPage
from pages import clockPage
from pages import weatherPage
from pages import calendarPage

class RaspiRoot(BoxLayout):
    carousel = ObjectProperty()

    # How often each page is updated in seconds
    # [clock, rss, weather, calendar]
    updateTimes = [1, 10, 120, 3600]

    # Current page number
    pageNr = 0
    pages = None

    def __init__(self, **kwargs):
        super(RaspiRoot, self).__init__(**kwargs)

        # Populate pages with a list of each page
        self.pages = self.carousel.slides

        # Iterate over pages and initialize them
        # NOTE: This requires all of the page classes
        # to have a function called "update"
        # and one called "nextClockCycle"
        for n, page in enumerate(self.pages):
            try:
                page.update()
                Clock.schedule_interval(page.nextClockCycle, self.updateTimes[n])
            except AttributeError:
                print("\nPages need to have update() and nextClockCycle() methods to work properly.\n")
                quit()

        # TODO: Change to the right slide when
        # the two sensors are triggered
        # Clock.schedule_interval(self.swipeRight, 3)

    # The dt is for testing purpose only,
    # remove when sensors are installed
    # Function to change slide
    # changes from left to right
    def swipeRight(self):
        self.pageNr = ( self.pageNr + 1 ) % len(self.pages)
        self.carousel.load_slide(self.pages[self.pageNr])

    # Function to change slide
    # changes from right to left
    def swipeLeft(self, dt):
        self.pageNr = ( self.pageNr - 1 ) % len(self.pages)
        self.carousel.load_slide(self.pages[self.pageNr])

class RaspiMirrorApp(App):
    pass

if __name__ == "__main__":
    RaspiMirrorApp().run()
