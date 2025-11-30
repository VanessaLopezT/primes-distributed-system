import redis
import psycopg2
import random
import math
import time
import os
# Conexiones

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB", "primesdb"),
    user=os.getenv("POSTGRES_USER", "primesuser"),
    password=os.getenv("POSTGRES_PASSWORD", "primespass")
)
conn.autocommit = True


# Prueba de primalidad EXACTA (divisores <= sqrt)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    limit = int(math.sqrt(n)) + 1

    for i in range(3, limit, 2):
        if n % i == 0:
            return False

    return True


# Generar número de N dígitos EXACTOS

def generate_number_with_digits(d: int) -> int:
    start = 10 ** (d - 1)
    end = (10 ** d) - 1
    return random.randint(start, end)


# Worker principal

def process_item(item: str):
    """
    item viene en este formato: "requestId:digitos"
    ejemplo: "80e9f3:12"
    """
    request_id, digits = item.split(":")
    digits = int(digits)

    while True:
        # Generar número
        candidate = generate_number_with_digits(digits)

        # Verificar primalidad exacta
        if not is_prime(candidate):
            continue

        # Verificar que NO esté repetido en la misma solicitud
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM primes WHERE request_id = %s AND prime_number = %s",
                (request_id, candidate)
            )
            exists = cur.fetchone()

            if exists:
                # número repetido → generar otro
                continue

            # Si no existe → Insertarlo y terminar
            cur.execute(
                "INSERT INTO primes (request_id, prime_number) VALUES (%s, %s)",
                (request_id, candidate)
            )
            break  # este item está completamente procesado


# Loop infinito del worker

if __name__ == "__main__":
    print("Worker iniciado...")

    while True:
        try:
            # Esperar un item
            item = redis_client.brpop("prime_queue", timeout=5)

            if item is None:
                continue

            _, value = item
            value = value.decode()

            print("Procesando:", value)
            process_item(value)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(1)
