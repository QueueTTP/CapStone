## kafka guide
##### 1. Install Kafka
```shell
(.venv) ➜  CapStone git:(qian) ✗ brew install kafka
```
==> Auto-updating Homebrew...
Adjust how often this is run with HOMEBREW_AUTO_UPDATE_SECS or disable with
HOMEBREW_NO_AUTO_UPDATE. Hide these hints with HOMEBREW_NO_ENV_HINTS (see `man brew`).
==> Auto-updated Homebrew!
Updated 3 taps (homebrew/services, homebrew/core and homebrew/cask).
==> New Formulae
dra                        firefly                    js-beautify                libblastrampoline          spidermonkey@115
fierce                     grizzly                    jsbeautifier               pyupgrade                  wush
==> New Casks
choice-financial-terminal  font-ibm-plex-math         font-lxgw-simzhisong       neo-network-utility        rize
crosspaste                 font-ibm-plex-sans-tc      font-scientifica           photostickies              winbox
flutterflow                font-lxgw-simxihei         gauntlet                   retcon                     xmenu

You have 16 outdated formulae installed.

Warning: kafka 3.8.0 is already installed and up-to-date.
To reinstall 3.8.0, run:
  brew reinstall kafka

##### 2. Start Zookeeper and Kafka
```shell
(.venv) ➜  CapStone git:(qian) ✗ brew services start zookeeper
```
==> Successfully started `zookeeper` (label: homebrew.mxcl.zookeeper)
```shell
(.venv) ➜  CapStone git:(qian) ✗ brew services start kafka
```
==> Successfully started `kafka` (label: homebrew.mxcl.kafka)

```shell check who's running, should see kafka and zookeeper
(.venv) ➜  CapStone git:(qian) ✗ brew services list
```
Name       Status     User File
jupyterlab none            
kafka      error  256 qian ~/Library/LaunchAgents/homebrew.mxcl.kafka.plist
zookeeper  error  256 qian ~/Library/LaunchAgents/homebrew.mxcl.zookeeper.plist

##### 3. Create a topic
```shell
(.venv) ➜  CapStone git:(qian) ✗ kafka-topics --create --topic event-simulation --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
Created topic event-simulation.

##### 4. List all topics (Verify)
```shell
(.venv) ➜  CapStone git:(qian) ✗ kafka-topics --list --bootstrap-server localhost:9092
```
__consumer_offsets
event-simulation
test

```code
# Kafka Producer
```python
from kafka import KafkaProducer
import json

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka server
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize Python dicts to JSON
)

# Function to send an event
def send_event(event_data):
    producer.send('event-simulation', event_data)
    print(f"Sent: {event_data}")

# Example usage
event = {"event_type": "E5", "celebrity": "Snoop Dogg", "description": "New social media post"}
send_event(event)

# Ensure all messages are sent
producer.flush()
```

```code
# Kafka Consumer
```python
from kafka import KafkaConsumer
import json

# Create a Kafka consumer
consumer = KafkaConsumer(
    'event-simulation',  # Topic name
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Start reading from the earliest messages
    enable_auto_commit=True,
    group_id='event_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
)

# Consume messages from Kafka
for message in consumer:
    event = message.value
    print(f"Received: {event}")
```

