import pika, sys, os
import json
import struct

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        with open('project/data.txt', 'r') as f:
            data = json.load(f)
            print(data)
        with open('project/data.txt', 'w') as f:
            lst = data['data']['quantity']
            labels = data['labels']
            label = int(labels[9])+1  # TODO: read last element, not 9
            lst.pop(0)
            lst.append(struct.unpack(">I", body)[0])
            labels.pop(0)
            labels.append(str(label))
            json.dump(data, f)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
