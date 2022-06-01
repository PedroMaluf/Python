import requests
from pprint import pprint


API_KEY = 'b4ceff0cdc4340d106862bfc9bce60f5'

city = input("City: ")

base_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + API_KEY + "&q=" + city

weather_data = requests.get(base_url).json()

pprint(weather_data)