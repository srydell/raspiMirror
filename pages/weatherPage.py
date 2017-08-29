# -*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import datetime
import json

class WeatherPage(BoxLayout):
    location = []
    pathToIcons = "./pages/weatherIcons/{}, {}.png"
    apiKey = ""
    conditions = ""
    temp = ""
    windSpeed = ""
    # TODO: Change browsing through conditions with regex and use this instead
    # config = {"location": [], "pathToIcons": "", "apiKey": "", "conditions": "", "temp": "", "windSpeed": ""}

    conditions_label = ObjectProperty()
    temp_label = ObjectProperty()
    conditions_image = ObjectProperty()
    wind_label = ObjectProperty()

    # Go to openweathermap.org to find weatherdata
    def __init__(self, **kwargs):
        super(WeatherPage, self).__init__(**kwargs)

        # TODO: Replace with regex
        # The api key is assumed to be the first line of secret.txt
        with open("secret.txt", "r") as secrets:
            self.apiKey = secrets.readline().rstrip("\n")
            location = secrets.readline().rstrip("\n")
            self.location = location.split()

    # Go to openweathermap.org to find weatherdata
    def update(self):
        weatherTemplate = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid=" + self.apiKey
        weatherUrl = weatherTemplate.format(*self.location)
        request = UrlRequest(weatherUrl, self.weatherParse)

    # Parse weatherdata
    def weatherParse(self, request, data):
        # Ensure that the data will be parsed even on
        # older versions of Kivy by using json (old bug)
        data = json.loads(data.decode()) if not isinstance(data, dict) else data

        # Parse the conditions
        cond = data["weather"][0]["description"]
        self.conditions = cond[0].upper() + cond[1:]

        # Parse the temperature
        # Round to one decimal and add degree symbol
        t = round(data["main"]["temp"], 1)
        t = "{} {}C".format(t, u"\u00b0".encode("utf-8"))
        self.temp = t

        # Parse the wind speed
        self.windSpeed = "{} m/s".format(data["wind"]["speed"])

        # Parse the data to decide if day or night
        # Will either be "day" or "night"
        daynight = self.dayOrNight(data["sys"]["sunset"])

        # Let conditions and day/night decide the icon
        self.pathToIcons = self.pathToIcons.format(self.conditions, daynight)

        self.conditions_label.text = self.conditions
        self.temp_label.text = self.temp
        self.wind_label.text = self.windSpeed
        self.conditions_image.source = self.pathToIcons

    def nextClockCycle(self, dt):
        self.update()

    def setTxtSize(self, txt, size):
        return "[size={}]{}[/size]".format(size, txt)

    # Check if it is day or night by comparing to timestamp of sunset
    def dayOrNight(self, sunsetTimestamp):
        sunset = datetime.datetime.fromtimestamp(sunsetTimestamp)
        now = datetime.datetime.now()
        untilSunset = (sunset - now).days

        # Will either be 0 : day or -1 : night
        # else failsafe to night
        if untilSunset == 0:
            return "day"
        else:
            return "night"

