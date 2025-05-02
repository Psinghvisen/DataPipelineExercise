from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

SERVICES = ["auth-service", "payment-service", "order-service"]

def generate_log():
    return {
        "service": random.choice(SERVICES),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status_code": random.choice([200, 201, 400, 404, 500]),
        "latency_ms": random.randint(100, 1500),
        "error": random.choice([False, True])
    }

if __name__ == "__main__":
    while True:
        log = generate_log()
        producer.send('service-logs', value=log)
        print("Produced:", log)
        time.sleep(1)
