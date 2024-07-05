FROM python:3.12.3-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY sample_app ./sample_app
COPY wsgi.py .
COPY gunicorn.conf.py .

ENTRYPOINT gunicorn wsgi:app
