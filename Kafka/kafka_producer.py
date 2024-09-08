import os
import random
import time
import json
from kafka import KafkaProducer
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from EventSim import EventSim

# create a producer object
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# send event
def send_event(event_data):
    producer.send('event-simulation', event_data)
    producer.flush()
    print(f'Event sent: {event_data}')


def run_event_sim_kafka(num_days = 180):
    for day in range(num_days):
        print(f"Simulating Day: {day+1}...")

        event = EventSim.choose_event()
        event_description = EventSim.event_descriptions.get(event,"Unknown Event")
        associated_celebrity = random.choice(EventSim.celebrities)

        event_data = {'event': event,
                      'event_description': event_description,
                      'associated_celebrity': associated_celebrity,
                      'day': day+1}
        
        print(f'Event {event} occurred ({event_description}), associated with {associated_celebrity}')

        send_event(event_data)

        time.sleep(10)
        
    print("Event Simulation Complete")


if __name__ == "__main__":
    run_event_sim_kafka(num_days=180)


