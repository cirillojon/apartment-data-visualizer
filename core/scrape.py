import requests
import os
import psycopg2
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Constants
URLS = [
    ("AMLI SLU", "https://www.amli.com/apartments/seattle/south-lake-union-apartments/amli-south-lake-union/floorplans"),
    ("AMLI Mark24", "https://www.amli.com/apartments/seattle/ballard-apartments/amli-mark24/floorplans"),
    ("AMLI 535", " https://www.amli.com/apartments/seattle/south-lake-union-apartments/amli-535/floorplans)")
]

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

def record_exists(cursor, table_name, floorplan_name, complex_id):
    query = f"""SELECT COUNT(*) FROM {table_name}
                WHERE floorplan_name = ? AND complex_id = ?"""
    cursor.execute(query, (floorplan_name, complex_id))
    count = cursor.fetchone()[0]
    return count > 0


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

def validate_floorplan_data(floorplan_data):
    """Validates the floorplan data."""
    essential_fields = ['floorplan_name', 'price']

    for field in essential_fields:
        if not floorplan_data[field]:
            return False
    return True

def insert_data_to_db(data_list, complex_name):
    try:
        with psycopg2.connect(dbname="apartments_db", user="postgres", password=POSTGRES_PASS, host="localhost", port="5432") as connection:
            with connection.cursor() as cursor:
                
                # Check if the complex exists and insert if not
                cursor.execute("SELECT complex_id FROM complexes WHERE complex_name = %s;", (complex_name,))
                complex_id = cursor.fetchone()
                if not complex_id:
                    cursor.execute("INSERT INTO complexes (complex_name) VALUES (%s) RETURNING complex_id;", (complex_name,))
                    complex_id = cursor.fetchone()[0]
                else:
                    complex_id = complex_id[0]

                # Check if table exists and create if not
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS apartments (
                        id SERIAL PRIMARY KEY,
                        floorplan_name VARCHAR(255) NOT NULL,
                        available_units INT,
                        bedrooms INT,
                        bathrooms INT,
                        size_range VARCHAR(255),
                        availability_date DATE,
                        price MONEY,
                        complex_id INT REFERENCES complexes(complex_id),
                        UNIQUE (floorplan_name, complex_id)
                    );
                """)

                # Remove duplicates from the table
                cursor.execute("""
                    DELETE FROM apartments a1
                    USING apartments a2
                    WHERE 
                        a1.floorplan_name = a2.floorplan_name AND
                        a1.complex_id = a2.complex_id AND
                        a1.id < a2.id;
                """)

                # Add the unique constraint if table already exists and the constraint does not
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.table_constraints 
                            WHERE constraint_name = 'unique_floorplan_complex'
                        ) THEN
                            ALTER TABLE apartments ADD CONSTRAINT unique_floorplan_complex UNIQUE (floorplan_name, complex_id);
                        END IF;
                    END
                    $$;
                """)

                for data in data_list:
                    # Only insert validated data
                    if validate_floorplan_data(data):
                        cursor.execute("""
                            INSERT INTO apartments (floorplan_name, available_units, bedrooms, bathrooms, size_range, availability_date, price, complex_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (floorplan_name, complex_id) 
                            DO UPDATE SET price = EXCLUDED.price, available_units = EXCLUDED.available_units;
                        """, (data['floorplan_name'], data['available_units'], data['bedrooms'], data['bathrooms'], data['size_range'], data['availability_date'], data['price'], complex_id))

        print("Data inserted or updated successfully!")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")



def scrape_and_insert():
    for complex_name, url in URLS:
        scraped_data = scrape_data(url)
        for data in scraped_data:
            for key, value in data.items():
                print(f"{key}: {value}")
            print("--------------------------")
        insert_data_to_db(scraped_data, complex_name)


# if __name__ == "__main__":
#     scrape_and_insert()