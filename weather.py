import requests
city = input("Enter the city:")
api_key = "api key"
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
response = requests.get(url)
if response.status_code == 200:
    weather_data = response.json()
    temp = weather_data["current"]["temp_c"]
    description = weather_data["current"]["condition"]["text"]
    print(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
