import json
from kafka import KafkaConsumer
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from EventSim import EventSim

# create a consumer object
consumer = KafkaConsumer('event-simulation',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='event_group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))


#update db kafka version
def update_db_kafka(connection, event):
    cursor = connection.cursor()

    event_type = event['event']
    celebrity = event['associated_celebrity']
    event_description = event['event_description']
    print(f'Processing {event_type} for {celebrity} : {event_description}')

    if event_type in EventSim.category_1_events: 
        EventSim.situation_category_1_event(connection, event_type,celebrity)
    elif event_type in EventSim.category_2_events:
        EventSim.situation_category_2_event(connection, event_type,celebrity)
    elif event_type in EventSim.category_3_events:
        EventSim.situation_category_3_event(connection, event_type,celebrity)
    elif event_type in EventSim.category_4_events:
        EventSim.situation_category_4_event(connection, event_type,celebrity)

    connection.commit()
    cursor.close()

# consume messages from kafka
def consume_events():
    connection = EventSim.create_connection()
    if connection is None or not connection.is_connected():
        print('Failed to MySQL database connection. Exiting...')
        return
    
    try:
        for message in consumer:
            event = message.value
            print(f"received event: {event}")
            
            if not connection.is_connected():
                print('Lost connection to MySQL database. Reconnect...')
                connection = EventSim.create_connection()
                if connection is None or not connection.is_connected():
                    print('Failed to MySQL database connection. Exiting...')
                    return
            update_db_kafka(connection, event)
    except Exception as e:
        print(f"Error consuming events: {str(e)}")
    finally:
        connection.close()
        print('Connection closed')



if __name__ == "__main__":
    consume_events()