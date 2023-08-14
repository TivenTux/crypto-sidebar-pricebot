FROM python:3.11

WORKDIR /crypto-sidebar-pricebot

COPY requirements.txt .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "./src/pricebot.py"]