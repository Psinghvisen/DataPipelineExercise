import json

# Load service config (latency thresholds, teams, etc.)
def load_config(config_path="config/service_config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

# Flag logs based on rules
def transform_log(log, config):
    service = log["service"]
    service_conf = config.get(service, {})

    latency_threshold = service_conf.get("latency_threshold", 1000)  # fallback
    log["is_slow"] = log["latency_ms"] > latency_threshold
    log["is_error"] = log["status_code"] >= 500
    return log

# Example batch transformation
def transform_logs_batch(logs, config_path="config/service_config.json"):
    config = load_config(config_path)
    return [transform_log(log, config) for log in logs]

# Example usage
if __name__ == "__main__":
    sample_logs = [
        {"service": "auth-service", "timestamp": "2025-04-30T10:01:00Z", "status_code": 500, "latency_ms": 1200, "error": True},
        {"service": "payment-service", "timestamp": "2025-04-30T10:01:01Z", "status_code": 200, "latency_ms": 300, "error": False}
    ]

    transformed = transform_logs_batch(sample_logs)
    for log in transformed:
        print(json.dumps(log, indent=2))
