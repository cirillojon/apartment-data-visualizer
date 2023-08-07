# Apartment Data Visualizer

This project scrapes apartment floorplan data from various websites and provides a visual representation of one-bedroom apartments, categorizing them based on price and size.

## Technologies Used

1. **React**: Frontend library used for building the user interface.
2. **Recharts**: React-based charting library used to create scatter plots.
3. **Flask**: A lightweight backend framework in Python to handle API requests and serve apartment data.
4. **PostgreSQL**: The relational database used to store apartment and complex details.
5. **Beautiful Soup**: A Python library for web scraping to pull data from apartment websites.
6. **APScheduler**: A Python job scheduling library, used to run the scraping task daily.
7. **dotenv**: A library to load environment variables from an `.env` file.

## Functionality

- **Web Scraping**: The `scrape.py` script fetches apartment details such as floorplan name, available units, bedrooms, bathrooms, size, availability date, and price from predefined URLs. Data validation functions ensure only meaningful data is considered.

- **Data Storage**: The scraped data is inserted into a PostgreSQL database, which has two main tables: `apartments` and `complexes`. Complex data is referenced in the apartment table using foreign keys. Duplication is avoided by having unique constraints in place.

- **API Endpoints**:
  - `/api/apartments`: Fetches apartment data by joining the `apartments` and `complexes` tables.
  - Test this `GET` request using: `curl http://127.0.0.1:5000/api/apartments`

- **Frontend (React)**:
  - Fetches data from the Flask API upon loading.
  - Filters and formats the data for 1-bedroom apartments.
  - Displays the data on a scatter plot where the x-axis represents the size (square footage) and the y-axis represents the price. Each apartment complex is color-coded, and hovering over a point provides more details about the apartment.

- **Background Task**: A daily scraping task is scheduled using APScheduler.

## Setup

1. **Environment Variables**: The project uses environment variables (stored in `.env` file) to securely handle database credentials.
2. **Database**: The PostgreSQL database must be set up with the name `apartments_db`, and the necessary tables (`apartments` and `complexes`) will be created by the scripts if they don't exist.

## Running the Application

- Start the Flask backend: 
  python app.py
- Start the React frontend: 
  npm start
