import pika, json
import os
"""
Este script publica mensajes a la cola de Rabbit MQ
"""

params = pika.URLParameters(os.environ.get('URL_NAME'))

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.exchange_declare('test_exchange')
channel.queue_declare(queue='test_queue')
channel.queue_bind('test_queue','test_exchange','test')
channel.queue_declare(queue='test_queue2')
channel.exchange_declare('test_exchange2')
channel.queue_bind('test_queue2','test_exchange2','test2')

def publish(body):
    channel.basic_publish(exchange='test_exchange', routing_key='test', body=json.dumps(body))
    channel.basic_publish(exchange='test_exchange2', routing_key='test2', body=json.dumps(body))
    print(json.dumps(body))
