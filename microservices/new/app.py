from fastapi import FastAPI
from pydantic import BaseModel
import redis
import psycopg2
import uuid

app = FastAPI()

# Redis
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Postgres connection
conn = psycopg2.connect(
    host="postgres",
    database="primesdb",
    user="postgres",
    password="postgres"
)
conn.autocommit = True

class RequestData(BaseModel):
    cantidad: int
    digitos: int

@app.post("/new")
def new_request(data: RequestData):
    # Crear ID único de solicitud
    request_id = str(uuid.uuid4())

    # Guardar solicitud en DB
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO requests (id, total_requested) VALUES (%s, %s)",
            (request_id, data.cantidad)
        )

    # Encolar solicitudes individuales
    for _ in range(data.cantidad):
        redis_client.lpush("prime_queue", f"{request_id}:{data.digitos}")

    return {"id": request_id}
