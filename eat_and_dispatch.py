from flask import Flask
from flask import request
from kafka import KafkaConsumer
from json import loads
import sys
import datetime
import send_colis as send_colis
import threading

custom_port = sys.argv[1]
app = Flask(__name__)

@app.route('/create_bio', methods=['POST'])
def prepare_biographics():

    colis_json = request.get_json()
    first_name = colis_json['first_name']
    name = colis_json['name']
    #picture = colis_json['picture']
    #bio_id = send_colis.create_new_biographics(first_name,name,picture)
    print (str(first_name) + " " + str(name) + " bien arrivé dans Insight")
    return str(bio_id +" created at " + datetime.datetime.now())


def start_REST_server(port) :
    print("Start REST SERVER on port  " + str(custom_port))
    app.run(host='0.0.0.0', port=port)

def start_kafka_consumer() :
    print("Start KAFKA CONSUMER wolalalalala")
    consumer = KafkaConsumer(
        'numtest',
        bootstrap_servers = ['localhost:8092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id = 'my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    for message in consumer :
        print(message.value)

if __name__ == '__main__':
    REST_thread = threading.Thread(target = start_REST_server, args=(custom_port,))
    kafka_thread = threading.Thread(target= start_kafka_consumer)

    REST_thread.start()
    kafka_thread.start()




