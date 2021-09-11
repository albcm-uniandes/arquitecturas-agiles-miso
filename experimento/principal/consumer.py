import pika, json

params = pika.URLParameters('amqps://yhqizdem:nJGBDLNceVinw90UAxBkIX-65Xw4aTWM@beaver.rmq.cloudamqp.com/yhqizdem')
connection = pika.BlockingConnection(params)
channel = connection.channel()
FILE_NAME = 'MOCK_DATA.json'
QUEUE = 'test_queue'
channel.queue_declare(queue=QUEUE)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(data)
    f = open(FILE_NAME, "a")
    f.write(json.dumps(data))
    f.close()


channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
