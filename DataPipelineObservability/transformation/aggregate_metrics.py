import numpy as np
from collections import defaultdict

def aggregate_metrics(logs):
    """
    Aggregates metrics per service.
    Input: List of logs (with latency_ms and is_error fields)
    Output: Dict with per-service metrics
    """
    service_groups = defaultdict(list)

    for log in logs:
        service = log["service"]
        service_groups[service].append(log)

    metrics = {}
    for service, svc_logs in service_groups.items():
        latencies = [log["latency_ms"] for log in svc_logs]
        errors = [log for log in svc_logs if log.get("is_error", False)]

        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        error_rate = len(errors) / len(svc_logs) if svc_logs else 0

        metrics[service] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "error_rate": round(error_rate, 4),
            "total_logs": len(svc_logs)
        }

    return metrics

# Example usage
if __name__ == "__main__":
    sample_logs = [
        {"service": "auth-service", "latency_ms": 350, "is_error": False},
        {"service": "auth-service", "latency_ms": 800, "is_error": True},
        {"service": "auth-service", "latency_ms": 700, "is_error": False},
        {"service": "payment-service", "latency_ms": 200, "is_error": False},
        {"service": "payment-service", "latency_ms": 500, "is_error": False}
    ]

    result = aggregate_metrics(sample_logs)
    for svc, m in result.items():
        print(f"\nService: {svc}")
        print(m)
