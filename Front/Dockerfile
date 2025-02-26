FROM python:3.8.5

WORKDIR /API

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app/main_page.py"]