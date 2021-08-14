import adafruit_dht
import board
import os
import sys
from utils.utils import *

dhtDevice = adafruit_dht.DHT22(board.D4)

def main():
    temp_diff = 1 #close windows before outside temp is greater than this modifier
    
    # hit weatherbit.io api
    outsideTemp_c = fetchOutsideTemp()
    outsideTemp_f = convertTofahrenheit(outsideTemp_c)
    print('outside temp', outsideTemp_f)

    try:
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
        
    except Exception as error:
        dhtDevice.exit()
        raise error

    if insideTemp_f < outsideTemp_f and not hasNotifiedToday('.open_window'):
        notify('.open_window')

    if insideTemp_f >= outsideTemp_f -temp_diff and not hasNotifiedToday('.close_window'):
        notify('.close_window')

main()
