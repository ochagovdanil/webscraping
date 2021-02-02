import requests
import time
import json
from playsound import playsound


# Suppress Trust SSL Certificate warnings
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# Some pre-defined constants
interval = 60
headers = {
    # Paste your headers here...
}
data = {
    # Paste your data here...
}


# Authorization
session = requests.Session()
response = session.put("https://ticket.bolshoi.ru/api/v1/client/login", headers=headers, data=data, verify=False)

if response.status_code != 200:
    exit()

# Requesting JSON data (seats)
url = input("Введите ссылку, по которой будет проходить мониторинг билетов: ").strip()
json_url = url.replace("show", "api/v1/client/shows") # Format to JSON URL
print("Приложение работает...(просьба не закрывать это окно)")


while True:
    try:
        # Sending requests in order to get two responses (old and new)
        response = session.get(json_url, headers=headers, data=data, verify=False)
        json_data = json.loads(response.text)
        number_of_seats = json_data["showInfo"]["freeSeats"]

        time.sleep(interval)

        response = session.get(json_url, headers=headers, data=data, verify=False)
        json_data = json.loads(response.text)
        new_number_of_seats = json_data["showInfo"]["freeSeats"]

        if new_number_of_seats > number_of_seats:
            playsound("notification.mp3")
            print("Новые билеты!") 
            continue
        else:
            continue
    except Exception:
        break
