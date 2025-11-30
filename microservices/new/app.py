from fastapi import FastAPI
from pydantic import BaseModel
import redis
import psycopg2
import uuid
import os
app = FastAPI()

# Conexión a Redis usando la variable de entorno
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    db=0
)
# Postgres connection
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB", "primesdb"),
    user=os.getenv("POSTGRES_USER", "primesuser"),
    password=os.getenv("POSTGRES_PASSWORD", "primespass")
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
