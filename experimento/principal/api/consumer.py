import os
import pika, json
params = pika.URLParameters(os.getenv('URL_NAME'))
connection = pika.BlockingConnection(params)
channel = connection.channel()
FILE_NAME = 'MOCK_DATA.json'
QUEUE = os.getenv('QUEUE_NAME')
channel.queue_declare(queue=QUEUE)
def callback(ch, method, properties, body):
    data = json.loads(body)
    f = open(FILE_NAME, "a")
    f.write(json.dumps(data)+','+'\n')
    f.close()


channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
