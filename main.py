import requests
import time
import json
import threading
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


# Collecting user data
number_of_urls = int(input("Введите количество ссылок (число), по которым будет происходить мониторинг: "))
json_url_array = []

for i in range(number_of_urls):
    url = input("Введите ссылку, по которой будет проходить мониторинг билетов: ").strip()
    json_url = url.replace("show", "api/v1/client/shows") # Format to JSON URL
    json_url_array.append(json_url)


def work(url):
    """ Requesting JSON data (free seats) """
    print("Запускаем мониторинг: " + url) 

    while True:
        try:
            # Sending requests in order to get two responses (old and new)
            response = session.get(url, headers=headers, data=data, verify=False)
            json_data = json.loads(response.text)
            number_of_seats = json_data["showInfo"]["freeSeats"]

            time.sleep(interval)

            response = session.get(url, headers=headers, data=data, verify=False)
            json_data = json.loads(response.text)
            new_number_of_seats = json_data["showInfo"]["freeSeats"]

            if new_number_of_seats > number_of_seats:
                print("Новые билеты по " + url)

                for i in range(3):
                    playsound("success.mp3")
                    time.sleep(1) 
        except Exception:
            print("\n\n!!!ВОЗНИКЛА НЕИЗВЕСТНАЯ ОШИБКА!!!")

            for i in range(5):
                playsound("error.mp3")
                time.sleep(1)

            exit()


# Spawning our threads
for i in json_url_array:
    t = threading.Thread(target=work, args=(i,))
    t.start()
    time.sleep(1)

print("Приложение работает...(просьба не закрывать окно)")
