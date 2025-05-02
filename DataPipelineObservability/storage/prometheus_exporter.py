from prometheus_client import start_http_server, Gauge
import random
import time

latency_gauge = Gauge('service_latency_ms', 'Service latency in ms', ['service'])
error_rate_gauge = Gauge('service_error_rate', 'Error rate', ['service'])

def push_metrics(service_data):
    for svc, data in service_data.items():
        latency_gauge.labels(service=svc).set(data['avg_latency'])
        error_rate_gauge.labels(service=svc).set(data['error_rate'])

if __name__ == "__main__":
    start_http_server(8000)  # Prometheus scrapes here
    while True:
        # Simulate
        sample = {
            "auth-service": {"avg_latency": random.randint(100, 500), "error_rate": random.random()},
            "payment-service": {"avg_latency": random.randint(200, 700), "error_rate": random.random()},
        }
        push_metrics(sample)
        time.sleep(5)
