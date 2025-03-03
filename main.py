import requests
from datetime import datetime
import os

# getting the current time
date = datetime.now()
current_date = str(date.date())
time =  date.time().strftime("%I:%M:%S")


# makesure to set envioment variable  to your keys 
# Nutritionxi API
APPLICATION_ID = os.environ["APPLICATION_ID"]
API_KEY =  os.environ["API_KEY"]






user_input = input ("Tell what exercise you did : ")

para = {
"query": user_input,
  "gender": "male",
  "weight_kg": 75,
  "height_cm": 184,
  "age": 22

}

header = {
    "x-app-id" : APPLICATION_ID,
    "x-app-key" :API_KEY,
    "Content-Type": "application/json"
}

response = requests.post (url="https://trackapi.nutritionix.com/v2/natural/exercise", headers=header, json=para)
response.raise_for_status()
data = response.json()["exercises"]

# adding formated date into  google spreadsheet
Bearer_code = os.environ["BEARER_CODE"]
spreadsheet_endpoint = os.environ["SPREADSHEET_ENDPOINT"]


for item in data :
    head ={
        "Authorization": Bearer_code
    }

    new_data = {
        "workout": {  # "workout" should match the sheet name or the name you defined in Sheety
            "date": current_date,
            "time" :  time,
            "exercise":  item["user_input"],
            "duration":  item["duration_min"],
            "calories": item["nf_calories"]
        }

    }
    reply = requests.post(url=spreadsheet_endpoint,
                          json=new_data,
                          headers=head)
    reply.raise_for_status()

