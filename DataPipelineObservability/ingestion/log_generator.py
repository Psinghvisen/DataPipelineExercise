from kafka import KafkaConsumer
import json
import os
from datetime import datetime

consumer = KafkaConsumer(
    'service-logs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id='log-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

log_dir = "data/raw_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"logs_{datetime.utcnow().date()}.json")

with open(log_file, 'a') as f:
    for msg in consumer:
        log = msg.value
        print("Consumed:", log)
        f.write(json.dumps(log) + "\n")
