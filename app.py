from flask import Flask
import redis
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("postgresql://postgres_redis_demo_user:aCQEoIHtWqv2yt0iMSsXQLfN5QEJWI1L@dpg-d4e1q2c9c44c73bhb5r0-a/postgres_redis_demo")
app = Flask(__name__)

# Redis 

r = redis.Redis(host = 'YOUR_REDIS_HOST', port=6379, db=0)

# PostgreSQL

conn = psycopg2.connect (
    host = "YOUR_POSTGRES_HOST",
    database = "YOUR_DB",
    user = "YOUR_USER",
    password = "YOUR_PASSWORD"
)

@app.route("/")
def hello():

    # Redis test
    r.set('foo', 'bar')
    val = r.get('foo').decode('utf-8')

    # PostgreSQL test
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.cclose()


    return f"Hello Render! Redis: {val}, Postgres: {result[0]}"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)

