import requests, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

POSTGRES_PASS = os.getenv('POSTGRES_PASS')

def extract_data(element, class_name):
    """Helper function to extract data and handle exceptions"""
    try:
        return element.find('div', class_=class_name).find_all('p')[1].text.strip()
    except (AttributeError, IndexError):
        return None
    
def extract_integer_from_string(s):
    """Extracts the first integer from a string."""
    if s:
        numbers = ''.join(filter(str.isdigit, s))
        if numbers:
            return int(numbers)
    return None

def extract_bedroom_count(s):
    """Converts bedroom descriptions into an integer."""
    if s == "Studio":
        return 0
    else:
        return extract_integer_from_string(s)
    
def extract_price(s):
    """Extracts price from a string and converts to float."""
    if s:
        # Removing dollar sign and any non-numeric characters except for digits and dots
        numbers = ''.join(filter(lambda x: x.isdigit() or x == '.', s.replace("$", "")))
        if numbers:
            return float(numbers)
    return None

URL = "https://www.amli.com/apartments/seattle/ballard-apartments/amli-mark24/floorplans"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

floorplans = soup.find_all('div', class_='floorplan-title-container')  # Each floorplan's starting point

# List to store scraped data
scraped_data = []

for floorplan in floorplans:
    data = {}
    data['floorplan_name'] = floorplan.find('h3', class_='floorplan-title').text if floorplan.find('h3', class_='floorplan-title') else None
    data['available_units'] = extract_integer_from_string(floorplan.find('h4', class_='floorplan-available-units').text) if floorplan.find('h4', class_='floorplan-available-units') else None
    
    # Directly finding the parent information container for the given floorplan title
    info_container = floorplan.find_next('div', class_='floorplan-information-container')
    
    data['bedrooms'] = extract_bedroom_count(extract_data(info_container, 'floorplan-info floorplan-beds'))
    data['bathrooms'] = extract_data(info_container, 'floorplan-info floorplan-baths')
    data['size_range'] = extract_data(info_container, 'floorplan-info floorplan-size')
    data['availability_date'] = extract_data(info_container, 'floorplan-info floorplan-availability')
    data['price'] = extract_price(extract_data(info_container, 'floorplan-info floorplan-pricing'))
    
    scraped_data.append(data)

    # Print the data
    for key, value in data.items():
        print(f"{key}: {value}")
    print("--------------------------")

import psycopg2

try:
    # Connecting to the DB
    connection = psycopg2.connect(
        dbname="apartments_db",
        user="postgres",
        password=POSTGRES_PASS,
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    # Inserting data into the database
    for data in scraped_data:
        cursor.execute("""
            INSERT INTO apartments (floorplan_name, available_units, bedrooms, bathrooms, size_range, availability_date, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (data['floorplan_name'], data['available_units'], data['bedrooms'], data['bathrooms'], data['size_range'], data['availability_date'], data['price']))

    # Committing transaction
    connection.commit()
    print("Data inserted successfully!")

except psycopg2.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection, even if an error occurred.
    if cursor:
        cursor.close()
    if connection:
        connection.close()
