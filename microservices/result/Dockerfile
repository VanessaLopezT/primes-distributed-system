FROM python:3.10-slim

WORKDIR /app

COPY app.py /app/

RUN pip install flask redis psycopg2-binary

EXPOSE 5002

CMD ["python", "app.py"]
