from datetime import datetime
from dotenv import load_dotenv
import json
import os
from pathlib import Path
import requests
from twilio.rest import Client

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#weatherbit env variables
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
url = f"https://api.weatherbit.io/v2.0/current?lat={LAT}&lon={LON}&key={API_KEY}&include=minutely"

# twilio env variables
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
FROM_ = os.getenv("FROM_")
TO_ = os.getenv("TO_")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def fetch_outside_temp():
  # grab the outside temp via weatherbit
  response = requests.get(url)
  data = json.loads(response.text)
  return data['data'][0]['temp']

def convert_to_fahrenheit(temp_c):
  # convert to Fahrenheit
  return (temp_c * (9 / 5)) + 32 

def has_notified_today(window_action):
  # test to see if file exists
  fname = Path(window_action)
  if fname.exists():
    return True
  return False

def action_type(window_action):
  # return either open or close to insert into text message
  if window_action == '.open_window':
    return 'open'
  return 'close'

def notify(window_action):
  # notify the user whether to open or close windows
  print(f'Take action: {window_action}')

  action = action_type(window_action)
  message = client.messages.create(
  to=TO_,
  from_=FROM_,
  body=f'It\'s time to {action} your windows.'
)
  # create a file that serves as a flag
  f = open(window_action, 'a')
  f.write('')
  f.close()
    
def cleanup_flag(flag):
  # remove the flag if it exists
  if os.path.exists(flag):
    os.remove(flag)
