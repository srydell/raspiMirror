# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

import kivy
kivy.require('1.9.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class CalendarPage(BoxLayout):
    calendar_label = ObjectProperty()
    eventDict = {'nEvents': 0, 'summary': [], 'location': [], 'start': [], 'end': []}

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = ''
    APPLICATION_NAME = 'CalendarPage'

    def __init__(self, **kwargs):
        super(CalendarPage, self).__init__(**kwargs)

        # TODO: Replace with regex
        with open("secret.txt", "r") as secrets:
            self.CLIENT_SECRET_FILE = secrets.readlines()[2]

    # Checks the calender and updates the label text
    def update(self):
        self.setEvents()
        summary = self.eventDict['summary']
        location = self.eventDict['location']
        start = self.eventDict['start']
        end = self.eventDict['end']
        for n in range(self.eventDict['nEvents']):
            formatting = "%H:%M"

            self.calendar_label.text += summary[n] + "\n"
            self.calendar_label.text += location[n] + "\n"
            self.calendar_label.text += start[n].strftime(formatting) + " - "
            # Formatted as (hours, minutes) tuple
            self.calendar_label.text += end[n].strftime(formatting) + "\n"

    # Repeates every clock cycle:
    # Starts update
    def nextClockCycle(self, dt):
        self.update()

    def getCredentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def setEvents(self):
        """
        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # Capture events within 24 hours
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        now = now.isoformat() + 'Z'
        tomorrow = tomorrow.isoformat() + 'Z' # 'Z' indicates UTC time

        # eventsResult = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        eventsResult = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        # TODO: Reformat start
        for event in events:
            summary = event['summary']
            location = event['location']

            # Format the start date of the event
            start = event['start'].get('dateTime', event['start'].get('date'))
            year = int(start[0:4])
            month = int(start[5:7])
            day = int(start[8:10])
            startHour = int(start[11:13])
            startMinute = int(start[14:16])
            durationHour = int(start[20:22])
            durationMinute = int(start[23:25])

            # Give start as a datetime object
            start = datetime.datetime(year, month, day, startHour, startMinute)
            end = datetime.datetime(year, month, day, startHour + durationHour, startMinute + durationMinute)

            # Add the event info to eventDict
            self.eventDict['summary'].append(summary)
            self.eventDict['location'].append(location)
            self.eventDict['start'].append(start)
            self.eventDict['end'].append(end)
            self.eventDict['nEvents'] += 1
