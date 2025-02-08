import os
import json
import requests
import subprocess
import datetime

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set! Please configure it in your environment.")

# API URL
CITY = "Montreal"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

log_file_path = 'logfile.txt'
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Open the log file in append mode
with open(log_file_path, 'a') as log_file:
    log_file.write(f'[{timestamp}] Script started\n')

# Fetch weather data
response = requests.get(URL)
if response.status_code != 200:
    print(f"Failed to get weather data: {response.text}")
    exit(1)

weather_data = response.json()

# Save data to a file
file_path = "weather_data.json"
with open(file_path, "w") as f:
    json.dump(weather_data, f, indent=4)

print(f"Weather data updated at {datetime.datetime.now()}")

# Git commands to commit and push changes
try:
    subprocess.run(["git", "add", file_path], check=True)
    subprocess.run(["git", "commit", "-m", f"Updated weather data at {datetime.datetime.now()}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Weather data pushed to GitHub successfully!")
except subprocess.CalledProcessError as e:
    print(f"Git error: {e}")

with open(log_file_path, 'a') as log_file:
    log_file.write(f'[{timestamp}] Script completed\n')
