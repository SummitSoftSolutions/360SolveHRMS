# from confluent_kafka import Producer
# import json
# KAFKA_CONFIG = {
#     'bootstrap.servers': 'localhost:9092'
# }

# producer = Producer(KAFKA_CONFIG)

# def send_hrm_event(event_type, **kwargs):
#     """Send HRM event to Kafka topic with dynamic parameters"""
#     event_data = {
#         "event_type": event_type,
<<<<<<< HEAD
#         **kwargs  # Include all extra key-value pairs
#     }
    
#     event_json = json.dumps(event_data)  # Convert to JSON
#     producer.produce('hrm-events', event_json.encode('utf-8'))
#     producer.flush()  # Ensure immediate delivery
#     print(f"HRM Event Sent: {event_json}")  # Debugging
=======
#         **kwargs  
#     }
    
#     event_json = json.dumps(event_data)  
#     producer.produce('hrm-events', event_json.encode('utf-8'))
#     producer.flush()  
#     print(f"HRM Event Sent: {event_json}")  
>>>>>>> a7d121cbe5e6aca323b6371fe845da5eef990110
