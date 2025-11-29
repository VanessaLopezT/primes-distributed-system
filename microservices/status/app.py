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

@app.get("/status/{request_id}")
def get_status(request_id: str):

    with conn.cursor() as cur:
        cur.execute("SELECT total_requested FROM requests WHERE id = %s", (request_id,))
        row = cur.fetchone()
        if not row:
            return {"error": "request not found"}
        
        total_requested = row[0]

        cur.execute("SELECT COUNT(*) FROM primes WHERE request_id = %s", (request_id,))
        current = cur.fetchone()[0]

    return {
        "total": total_requested,
        "actual": current
    }
