import requests
from bs4 import BeautifulSoup

URL = "https://www.amli.com/apartments/seattle/ballard-apartments/amli-mark24/floorplans" 
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting data
floorplan_name = soup.find('h3', class_='floorplan-title').text
available_units = soup.find('h4', class_='floorplan-available-units').text
bedrooms = soup.find('div', class_='floorplan-info floorplan-beds').find_all('p')[1].text
bathrooms = soup.find('div', class_='floorplan-info floorplan-baths').find_all('p')[1].text
size = soup.find('div', class_='floorplan-info floorplan-size').find_all('p')[1].text
availability_date = soup.find('div', class_='floorplan-info floorplan-availability').find_all('p')[1].text
price = soup.find('div', class_='floorplan-info floorplan-pricing').find_all('p')[1].text

# Print out the data
print(f"Floorplan Name: {floorplan_name}")
print(f"Available Units: {available_units}")
print(f"Bedrooms: {bedrooms}")
print(f"Bathrooms: {bathrooms}")
print(f"Size: {size}")
print(f"Availability Date: {availability_date}")
print(f"Price: {price}")
