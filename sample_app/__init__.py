import time

from flask import Flask
from opentelemetry.metrics import get_meter

def create_app():
    app = Flask(__name__)

    meter = get_meter(__name__)
    request_count = meter.create_counter("requests.count")

    @app.get("/")
    def index():
        request_count.add(1)
        time.sleep(2)
        return "<h2>Hello World!</h2>"
    return app
