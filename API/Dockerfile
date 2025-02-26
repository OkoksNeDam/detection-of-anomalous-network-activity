FROM python:3.8.5

WORKDIR /API

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --default-timeout=900 -r requirements.txt

COPY . .

CMD ["python", "-m", "api"]