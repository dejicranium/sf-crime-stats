from kafka import KafkaConsumer
import json
import time

topic_name = "com.deji.stream.crimes"


def deserialize(json_data):
    return json.loads(json_data.decode('ascii'))


consumer = KafkaConsumer(
    topic_name, 
    auto_offset_reset='earliest',
    group_id='consumer-group', 
    bootstrap_servers=['localhost:9092'],
    value_deserializer=deserialize,
    consumer_timeout_ms=3000)


#subscribe
consumer.subscribe([topic_name])

while True:
    message = None
    try:
        message = consumer.poll(timeout_ms=1, max_records=1000)
    except Exception as e:
        print("Error " , e)
    print(message)
    
    time.sleep(1)
        