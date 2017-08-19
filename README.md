# RaspiMirror

This is a small hardware/software project to get a somewhat smart desk gadget. It will be a screen with a number of pages that can be navigated by swiping your hand through the air. The hand movements will be captured using two IR sensors.

## Getting Started

Here is the list of hardware used:

* Raspberry Pi Zero W
* 3.5" Screen
* 2 IR sensors

The GUI is run by [kivy](https://kivy.org/#home) and is downloadable for your system [here](https://kivy.org/#download).
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Assuming you have installed kivy it is now time to get the dependencies. The feedparser package is used for parsing the RSS data. This can be installed by running:

```
$ kivy -m pip install feedparser
```

To install the Google API run this in your shell:

```
$ kivy -m pip install --upgrade google-api-python-client
```

### Installing

Download the content by running

$ git clone git://github.com/srydell/raspiMirror.git

Change directory and start the program. How to run a kivy program is different for Mac/(linux/windows) users.

``` For Mac users:

$ cd raspiMirror
$ kivy main.py

``` For linux/windows users:

$ python main.py