from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from core.settings import get_settings


def setup_tracing():
    settings = get_settings()
    otlp_endpoint = settings.otlp_endpoint
    resource = Resource.create(
        {
            "service.name": settings.service_name,
        }
    )

    provider = TracerProvider(resource=resource)

    # 1️⃣ Always enable console exporter (dev-friendly)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    # 2️⃣ Optional OTLP exporter (collector, Tempo, etc.)
    if otlp_endpoint != "":
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
        )

    trace.set_tracer_provider(provider)
