import pika, json

"""
Este script publica mensajes a la cola de Rabbit MQ
"""

params = pika.URLParameters('amqps://yhqizdem:nJGBDLNceVinw90UAxBkIX-65Xw4aTWM@beaver.rmq.cloudamqp.com/yhqizdem')

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.exchange_declare('test_exchange')
channel.queue_declare(queue='test_queue')
channel.queue_bind('test_queue','test_exchange','test')

def publish(body):
    channel.basic_publish(exchange='test_exchange', routing_key='test', body=json.dumps(body))
