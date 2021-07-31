import adafruit_dht
import board
import os
import sys
import time
from utils.utils import *

dhtDevice = adafruit_dht.DHT22(board.D4)

def main():
    # check sql table
    while True:
        try:
            outsideTemp_c = fetchOutsideTemp()
            print('outside celcius', outsideTemp_c)
            outsideTemp_f = convertTofahrenheit(outsideTemp_c)
            print('outside temp', outsideTemp_f)

            # Print the values to the serial port
            insideTemp_c = dhtDevice.temperature
            insideTemp_f = convertTofahrenheit(insideTemp_c)
            humidity = dhtDevice.humidity
            print(
                "Inside Temp: {:.1f} F / {:.1f} C Humidity: {}% ".format(
                    outsideTemp_f, outsideTemp_c, humidity
                )
            )

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        # check temp every 3 minutes
        time.sleep(180)

main()