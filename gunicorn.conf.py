import socket
import uuid

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

bind = "0.0.0.0:4000"
reload = True
threads = 5
workers = 5


def post_fork(server, worker):
    server.log.info("worker spawned (pid: %s)", worker.pid)
    uid = uuid.uuid4().hex[0:8]

    resource = Resource.create(attributes={
        "service.name": "sample-app",
        "service.instance.id": f"{socket.gethostname()}:{uid}"
    })

    metric_reader = PeriodicExportingMetricReader(
            exporter=OTLPMetricExporter(endpoint="http://otel-col:4317"),
            export_interval_millis=5000,
    )
    metric_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
    metrics.set_meter_provider(metric_provider)
