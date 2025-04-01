# from confluent_kafka import Consumer, KafkaException

# KAFKA_CONFIG = {
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': 'hrm-group',
#     'auto.offset.reset': 'earliest'
# }

# consumer = Consumer(KAFKA_CONFIG)
# consumer.subscribe(['hrm-events'])

# def consume_hrm_events():
#     try:
#         while True:
#             msg = consumer.poll(1.0)  # Poll every second
#             if msg is None:
#                 continue
#             if msg.error():
#                 raise KafkaException(msg.error())
#             print(f"Received HRM Event: {msg.value().decode('utf-8')}")
#     finally:
#         consumer.close()
