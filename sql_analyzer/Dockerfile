FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY sql_analyzer.py /app
COPY /sql/ /app/sql/

ENV NUM_ATTEMPTS=20

CMD ["python", "sql_analyzer.py"]