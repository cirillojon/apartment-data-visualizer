from flask import Flask, jsonify
from scrape import scrape_and_insert
from apscheduler.schedulers.background import BackgroundScheduler
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
POSTGRES_PASS = os.getenv('POSTGRES_PASS')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/apartments', methods=['GET'])
def get_apartments():
    try:
        with psycopg2.connect(dbname="apartments_db", user="postgres", password=POSTGRES_PASS, host="localhost", port="5432") as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM apartments;")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                return jsonify(result)
    except psycopg2.Error as e:
        return jsonify({"error": str(e)})

def scheduled_scrape():
    scrape_and_insert()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_scrape, trigger="interval", days=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
