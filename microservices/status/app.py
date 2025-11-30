from fastapi import FastAPI
import psycopg2
import os
app = FastAPI()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB", "primesdb"),
    user=os.getenv("POSTGRES_USER", "primesuser"),
    password=os.getenv("POSTGRES_PASSWORD", "primespass")
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
