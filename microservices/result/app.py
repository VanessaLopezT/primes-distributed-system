from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    host="postgres",
    database="primesdb",
    user="postgres",
    password="postgres"
)
conn.autocommit = True

@app.get("/result/{request_id}")
def get_result(request_id: str):

    with conn.cursor() as cur:
        cur.execute(
            "SELECT prime_number FROM primes WHERE request_id = %s ORDER BY id ASC",
            (request_id,)
        )
        rows = cur.fetchall()

    primes = [int(r[0]) for r in rows]

    return primes
