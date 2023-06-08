# Wiba calculator tool - this tool calculates the time needed to reach the leader of the current race of the zakstunts.hu website.
# This tool was developed by Erik Barros and Duplode
# Updated version to get all racers

import requests
from bs4 import BeautifulSoup

# Make a GET request to the main website
main_page = requests.get('https://zak.stunts.hu')


# Parse the HTML content of the main page using BeautifulSoup to find the track link
soup_main = BeautifulSoup(main_page.content, 'html.parser')

current_status = soup_main.find(class_='cr-track-details')

current_race = current_status.find_all(href=True)[0]

string1 = str(current_race['href'])

link = "https://zak.stunts.hu" + string1

# Make a GET request to the website URL current track
response = requests.get(link)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the data element using its HTML class
scoreboard_data = soup.find(class_='scoreboard')

coeffs_data = soup.find(class_='coeffs-and-map')
car_elements = coeffs_data.select('.sc-label')
value_elements = coeffs_data.select('.sc-value')

cars = [car.text.strip() for car in car_elements]
values = [float(value.text.strip().rstrip('%')) / 100 for value in value_elements]

car_values = list(zip(cars, values))

# Find all racer data elements using their HTML class
racer_data = scoreboard_data.find_all(class_='racer')
time_data = scoreboard_data.find_all(class_='time')
car_data = [car.find(class_='car-image')['alt'] for car in scoreboard_data.find_all(class_='car')]

# Create a dictionary to store racer times
racer_times = {}
racer_car = {}

# Extract racer names, times and cars
for racer, time, car in zip(racer_data, time_data, car_data):
    racer_name = racer.text.strip()
    racer_times[racer_name] = (time)
    racer_car[racer_name] = (car)

# Display menu to choose the racer
print("Select a racer time to calculate the bonus:")
for i, racer_name in enumerate(racer_times.keys()):
    print(f"{i+1}. {racer_name}")

# Prompt user for input
choice = int(input("Enter the racer number: "))

# Calculate the time based on the chosen racer time
chosen_racer = list(racer_times.keys())[choice-1]
chosen_time = (racer_times[chosen_racer])
chosen_car = racer_car[chosen_racer]

time_string = chosen_time.text.strip().split()[0]
minutes, seconds = map(float, time_string.split(':'))
time_float = minutes * 60 + seconds

time = chosen_time.text

# Print the extracted data
print(f"--------You Choose-------------")
print(f"Racer: {chosen_racer}")
print(f"Car: {chosen_car}")
print(f"Time: {time}")

racer_value = None

for i, car in enumerate(cars):
    if car == chosen_car:
        racer_value = values[i]
        break

if racer_value is not None:
    print(f"--------Goal Times-------------")
    
# Calculate car coefficients
    for car, value in car_values:
        calc_total = (time_float / (1 - value)) - 0.05
        calc_frame = int(calc_total * 20)
        calc_min = calc_frame // 1200
        calc_remainder = calc_frame % 1200
        calc_seg = calc_remainder // 20
        calc_centi = 5 * (calc_remainder % 20)
        print(f"{car}: {calc_min}:{calc_seg:02}.{calc_centi:02}")
        
else:
    print("Car value not found in the table")

print(f"-------------------------------")    
print("Go catch em")
input("Press Enter to quit")