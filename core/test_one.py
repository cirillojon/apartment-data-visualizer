import requests
from bs4 import BeautifulSoup

def extract_data(element, class_name):
    """Helper function to extract data and handle exceptions"""
    try:
        return element.find('div', class_=class_name).find_all('p')[1].text.strip()
    except (AttributeError, IndexError):
        return None

URL = "https://www.amli.com/apartments/seattle/downtown-seattle-apartments/amli-arc/floorplans"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

floorplans = soup.find_all('div', class_='floorplan-title-container')  # Each floorplan's starting point

for floorplan in floorplans:
    floorplan_name = floorplan.find('h3', class_='floorplan-title').text if floorplan.find('h3', class_='floorplan-title') else None
    available_units = floorplan.find('h4', class_='floorplan-available-units').text if floorplan.find('h4', class_='floorplan-available-units') else None
    
    # Directly finding the parent information container for the given floorplan title
    info_container = floorplan.find_next('div', class_='floorplan-information-container')
    
    bedrooms = extract_data(info_container, 'floorplan-info floorplan-beds')
    bathrooms = extract_data(info_container, 'floorplan-info floorplan-baths')
    size = extract_data(info_container, 'floorplan-info floorplan-size')
    availability_date = extract_data(info_container, 'floorplan-info floorplan-availability')
    price = extract_data(info_container, 'floorplan-info floorplan-pricing')

    # Print out the data
    print("------ Floorplan Details ------")
    print(f"Floorplan Name: {floorplan_name}")
    print(f"Available Units: {available_units}")
    print(f"Bedrooms: {bedrooms}")
    print(f"Bathrooms: {bathrooms}")
    print(f"Size: {size}")
    print(f"Availability Date: {availability_date}")
    print(f"Price: {price}\n")