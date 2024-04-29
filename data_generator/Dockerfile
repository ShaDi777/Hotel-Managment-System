FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY data_generator.py /app

ENV NUM_RECORDS=1100000

CMD ["python", "data_generator.py"]