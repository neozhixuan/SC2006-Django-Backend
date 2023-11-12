import requests

x = requests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast')

print(x.text)
