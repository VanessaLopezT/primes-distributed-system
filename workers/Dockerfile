FROM python:3.10-slim

WORKDIR /worker

COPY worker.py /worker/

RUN pip install redis psycopg2-binary

CMD ["python", "worker.py"]
