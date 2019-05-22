import threading
from json import loads
from flask import Flask
from flask import request
from kafka import KafkaConsumer
import os
import logging
import send_colis as send_colis

# with open(sys.argv[1], 'r') as file :
#     param = yaml.load(file)

debug_level = os.environ["DEBUG_LEVEL"]

if debug_level == "DEBUG" :
    logging.basicConfig(level=logging.DEBUG)
elif debug_level == "INFO" :
    logging.basicConfig(level=logging.INFO)
elif debug_level == "WARNING" :
    logging.basicConfig(level=logging.WARNING)
elif debug_level == "ERROR" :
    logging.basicConfig(level=logging.ERROR)
elif debug_level == "CRITICAL" :
    logging.basicConfig(level=logging.CRITICAL)


colissithon_port = os.environ["COLISSITHON_PORT"]
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])
print("########### KAFKA ENDPOINT IS :  " + kafka_endpoint)
app = Flask(__name__)


@app.route('/create_bio', methods=['POST'])
def prepare_biographics():
    logging.info('create_bio service called')
    colis_json = request.get_json()
    first_name = colis_json['biographicsFirstName']
    name = colis_json['biographicsName']
    logging.debug('creation of biographics for ' + str(first_name) + " " + str(name))
    picture = colis_json['biographicsImage']
    picture_type = colis_json['biographicsImageContentType']
    bio_id = send_colis.create_new_biographics(first_name, name, picture, picture_type)
    return str(bio_id)


def start_REST_server(port):
    app.run(host='0.0.0.0', port=port)


def start_tweets_consumer():
    consumer = KafkaConsumer(
        'tweetopic',
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for Tweetopic started')
    for msg in consumer:
        logging.debug('Consume message from ##Tweetopic')
        tweet_json = msg.value[0]
        bio_id = msg.value[1]
        logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
        send_colis.link_tweet_to_bio(tweet_json, bio_id)


def start_pictures_consumer():
    consumer = KafkaConsumer(
        'topictures',
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for Topictures started')
    for msg in consumer:
        logging.debug('Consume message from ##Topictures')
        picture_json = msg.value[0]
        bio_id = msg.value[1]
        logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
        send_colis.link_picture_to_bio(picture_json, bio_id)


if __name__ == '__main__':
    REST_thread = threading.Thread(target=start_REST_server, args=(colissithon_port,))
    rawdatas_thread = threading.Thread(target=start_tweets_consumer)
    pictures_thread = threading.Thread(target=start_pictures_consumer)

    REST_thread.start()
    logging.info('REST Thread started')
    rawdatas_thread.start()
    logging.info('Kafka Tweetopic Thread started')
    pictures_thread.start()
    logging.info('Kafka Topictures Thread started')
