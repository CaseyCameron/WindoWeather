import adafruit_dht
import board
import os
import sys
from utils.utils import *

dhtDevice = adafruit_dht.DHT22(board.D4)

def main():
    temp_diff = 1 #close windows before outside temp is greater than this modifier
    
    # hit weatherbit.io api
    outside_temp_c = fetch_outside_temp()
    outside_temp_f = convert_to_fahrenheit(outside_temp_c)
    print('outside temp', outside_temp_f)

    try:
        # Print the values to the serial port
        inside_temp_c = dhtDevice.temperature
        inside_temp_f = convert_to_fahrenheit(inside_temp_c)
        humidity = dhtDevice.humidity
        print(
            "Inside Temp: {:.1f} F / {:.1f} C Humidity: {}% ".format(
                outside_temp_f, outside_temp_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        
    except Exception as error:
        dhtDevice.exit()
        raise error

    if inside_temp_f < outside_temp_f and not has_notified_today('.open_window'):
        notify('.open_window')

    if inside_temp_f >= outside_temp_f -temp_diff and not has_notified_today('.close_window'):
        notify('.close_window')

main()
