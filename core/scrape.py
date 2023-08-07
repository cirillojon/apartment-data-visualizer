import requests
import os
import psycopg2
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Constants
URL = "https://www.amli.com/apartments/seattle/ballard-apartments/amli-mark24/floorplans"

# Load environment variables
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
        numbers = ''.join(filter(lambda x: x.isdigit() or x == '.', s.replace("$", "")))
        if numbers:
            return float(numbers)
    return None

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    floorplans = soup.find_all('div', class_='floorplan-title-container')

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
    
    return scraped_data

def insert_data_to_db(data_list):
    try:
        with psycopg2.connect(dbname="apartments_db", user="postgres", password=POSTGRES_PASS, host="localhost", port="5432") as connection:
            with connection.cursor() as cursor:
                
                # Check if table exists and create if not
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS apartments (
                    id SERIAL PRIMARY KEY,
                    floorplan_name VARCHAR(255),
                    available_units INT,
                    bedrooms INT,
                    bathrooms INT,
                    size_range VARCHAR(255),
                    availability_date DATE,
                    price MONEY
                );
                """)

                for data in data_list:
                    cursor.execute("""
                        INSERT INTO apartments (floorplan_name, available_units, bedrooms, bathrooms, size_range, availability_date, price)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (data['floorplan_name'], data['available_units'], data['bedrooms'], data['bathrooms'], data['size_range'], data['availability_date'], data['price']))

        print("Data inserted successfully!")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

def main():
    scraped_data = scrape_data(URL)
    
    for data in scraped_data:
        for key, value in data.items():
            print(f"{key}: {value}")
        print("--------------------------")
        
    insert_data_to_db(scraped_data)

if __name__ == "__main__":
    main()
