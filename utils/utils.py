from datetime import datetime
from dotenv import load_dotenv
import json
import os
from pathlib import Path
import requests

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
url = f"https://api.weatherbit.io/v2.0/current?lat={LAT}&lon={LON}&key={API_KEY}&include=minutely"

def fetchOutsideTemp():
  response = requests.get(url)
  data = json.loads(response.text)
  return data['data'][0]['temp']

def convertTofahrenheit(temp_c):
  return (temp_c * (9 / 5)) + 32 

def hasNotifiedToday(window_action):
  # test to see if file exists
  fname = Path(window_action)

  if fname.exists():
    return True
  return False

def notify(window_action):
  print(f'Take action: {window_action}')
  # create a file that serves as a flag
  f = open(window_action, 'a')
  f.write('')
  f.close()
    
def cleanupFlag(flag):
  if os.path.exists(flag):
    os.remove(flag)