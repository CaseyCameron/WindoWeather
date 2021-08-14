# WindoWeather Overview

* WindoWeather utilizes a raspberry pi and a dht22 temperature sensor to compare indoor/outdoor temperatures.
* It will notify users via sms when it's time to open or close windows.
* It uses the [weatherbit.io](https://www.weatherbit.io/) api to check outdoor temperatures.
* It uses [twilio](https://twilio.com) for sms.
* The dht22 sensor code and pin setup was taken and adapted from [this](https://medium.com/initial-state/how-to-build-a-raspberry-pi-temperature-monitor-8c2f70acaea9) article.
* The rest of the logic was written by me.
----
* WindoWeather is setup to run every three minutes, comparing temperatures.
  * It does this with a cron job
  * The free version of [weatherbit.io](https://www.weatherbit.io/) has a call limit. This is why WindoWeather only runs every 3 minutes. 
  * You can setup WindoWeather to run as often as you want. 
----
* Once WindoWeather detects a temperature change it notifies the user via sms and creates a hidden file to acts as a toggle.
* WindoWeather continues to run, but if the hidden file exists it will not notify the user.
* A second cron job is necessary each morning to run the cleanup.py script. 
  * This will "restart" the app which allows it to notify the user of a temperature difference.
  * This logic is necessary so that the user isn't notifed after the initial notification that AM or PM.
----
## Requirements: 
* An account with [weatherbit.io](https://www.weatherbit.io/)
* An api key, and your gps coordinates
  * .env variables setup as:
    - API_KEY
    - LAT
    - LON
* An account with [twilio](https://twilio.com)
* An api key, an auth token, a twilio #, your mobile number
  * .env variables setup as:
    - ACCOUNT_SID
    - AUTH_TOKEN
    - FROM_
    - TO_
* A raspberry pi version 3 or higher
* A DHT22 temperature sensor
  * The 5V pin connects to pin 2 on the pi
  * The GND pin connects to pin 6 of the pi.
  * The Data pin connects to GPIO4, or pin 7 of the pi.
* Setup two cron jobs as follows [(here's a cron timer helper)](https://crontab.guru/): 
  * First, run the cleanup in the morning. Set this for whenever you want to begin comparing temperatures in the AM. Mine is set to 7am.
    * Fill in the path to python, and the path to the app.
      - 0 7 * * * /PATH_TO_/python /PATH_TO_/WindoWeather/cleanup.py
  * Second, set a job to run the program every three minutes (or however often you choose - careful of api call limits)
      - */3 * * * * /PATH_TO_/python /PATH_TO_/WindoWeather/main.py > /tmp/cronjob.log 2>&1
----
If you are unfamiliar with cron jobs please read a tutorial overview. When you want this program to stop running, you will need to remove these cron jobs.
----
# Disclaimer
This is a personal project. The author does not assume any responsibility. Use at your own discretion. Be aware of sms limits with your provider and Twilio.
Be aware of the importance of setting up the cron jobs properly in order to avoid constant notifications. 
