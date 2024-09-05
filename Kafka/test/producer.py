from kafka import KafkaProducer
import json

#create a producer object
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

#send event
def send_event(event_data):
    producer.send('event-simulator', event_data)
    print(f'Event sent: {event_data}')

#example usage
event = {'event_type':'E5',
         'celebrity':'Snoop Dogg',
         'description':'New social media post'}
send_event(event)

#ensure all messages are sent before closing the producer
producer.flush()