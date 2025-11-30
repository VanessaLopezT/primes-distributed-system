CREATE TABLE IF NOT EXISTS requests (
    id VARCHAR(100) PRIMARY KEY,
    total_requested INT NOT NULL
);

CREATE TABLE IF NOT EXISTS primes (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(100) NOT NULL,
    prime_number BIGINT NOT NULL,
    UNIQUE(request_id, prime_number),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);
