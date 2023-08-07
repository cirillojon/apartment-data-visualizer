import os, psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASS = os.getenv('POSTGRES_PASS')

# Connecting to the DB
connection = psycopg2.connect(
    dbname="apartments_db",
    user="postgres",
    password=POSTGRES_PASS,
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Retrieving data from the database
cursor.execute("SELECT * FROM apartments;")
rows = cursor.fetchall()

# Displaying data
print("ID | Floorplan Name | Available Units | Bedrooms | Bathrooms | Size Range | Availability Date | Price")
print("-"*110)
for row in rows:
    # Check if the price value is a float or int type, if not, display as-is
    price = f"${row[7]:,.2f}" if isinstance(row[7], (float, int)) else row[7]
    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {price}")

# Closing connection
cursor.close()
connection.close()
