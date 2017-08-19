# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import feedparser
import datetime
import json

class RssPage(BoxLayout):
    rss_label = ObjectProperty()
    listOfRSS = []

    # Sets self.listOfRSS to a fetched list of RSS headlines
    def fetchFeed(self):
        rssUrl = "feed://rss.nytimes.com/services/xml/rss/nyt/World.xml"

        # request = UrlRequest(rssUrl, self.rssParse)
        rss = feedparser.parse(rssUrl)

        # Create a list of all summaries from the rss feed
        self.listOfRSS = [entry["summary"] for entry in rss["entries"] if len(entry["summary"]) > 0]

    # Returns the next story in listOfRSS
    # If listOfRSS empty -> fetchRSS()
    def update(self):
        if len(self.listOfRSS) > 0:
            headLine = self.listOfRSS.pop()
            self.rss_label.text = headLine
        else:
            self.fetchFeed()
            headLine = self.listOfRSS.pop()
            self.rss_label.text = headLine

    # Repeates every clock cycle:
    # Sets the label text to the next
    # story by using self.setNextRSS()
    def nextClockCycle(self, dt):
        self.update()
