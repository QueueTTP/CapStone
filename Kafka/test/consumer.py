from kafka import KafkaConsumer
import json


# create a consumer object
consumer = KafkaConsumer('event-simulation',
                         bootstrap_servers='localhost:9092',
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            group_id='event_group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# consume messages from kafka
for message in consumer:
    event = message.value
    print(f"received event: {event}")
