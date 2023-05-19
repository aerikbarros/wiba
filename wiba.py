# Wiba calculator tool - this tool calculates the time needed to reach the leader of the current race of the zakstunts.hu website.
# This tool was developed by Erik Barros and Duplode

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

# Find the inner class inside the outer class using a CSS selector to get racer and car
time_data = scoreboard_data.select_one('.time')
racer_data = scoreboard_data.select_one('.racer')
lead_car = scoreboard_data.select_one('.car-image')['alt']

time_string = time_data.text.strip().split()[0]
minutes, seconds = map(float, time_string.split(':'))

time = time_data.text
racer = racer_data.text

# Convert minutes to seconds
time_float = minutes * 60 + seconds

cars = [car.text.strip() for car in car_elements]
values = [float(value.text.strip().rstrip('%')) / 100 for value in value_elements]

car_values = list(zip(cars, values))

# Print the extracted data
print(f"Lead racer: {racer}")
print(f"Lead car: {lead_car}")
print(f"Lead time: {time}")

leader_value = None

for i, car in enumerate(cars):
    if car == lead_car:
        leader_value = values[i]
        break

if leader_value is not None:
    print(f"--------Goal Times-------------")
    
# Calculate car coefficients
    for car, value in car_values:
        calc_total = time_float / (1 - value)
        calc_frame = int(calc_total * 20)
        calc_min = calc_frame // 1200
        calc_remainder = calc_frame % 1200
        calc_seg = calc_remainder // 20
        calc_centi = 5 * (calc_remainder % 20)
        print(f"{car}: {calc_min}:{calc_seg:02}.{calc_centi:02}")
else:
    print("Leader's car value not found in the table")
