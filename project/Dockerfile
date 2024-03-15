FROM python:3.6

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

COPY static static

CMD ["python", "app.py"]
