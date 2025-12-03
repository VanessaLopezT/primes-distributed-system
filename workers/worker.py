import redis
import psycopg2
import random
import math
import time
import os

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB", "primesdb"),
    user=os.getenv("POSTGRES_USER", "primesuser"),
    password=os.getenv("POSTGRES_PASSWORD", "primespass")
)
conn.autocommit = True

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

def generate_number_with_digits(d: int) -> int:
    start = 10 ** (d - 1)
    end = (10 ** d) - 1
    return random.randint(start, end)


def process_item(item: str):
    request_id, digits = item.split(":")
    digits = int(digits)

    while True:
        candidate = generate_number_with_digits(digits)

        if not is_prime(candidate):
            continue

        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM primes WHERE request_id = %s AND prime_number = %s",
                (request_id, candidate)
            )

            exists = cur.fetchone()

            if exists:
                continue

            cur.execute(

                "INSERT INTO primes (request_id, prime_number) VALUES (%s, %s)",
                (request_id, candidate)
            )

            break


if __name__ == "__main__":
    print("Worker iniciado...")

    while True:
        try:
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
