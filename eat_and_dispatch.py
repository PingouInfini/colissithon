import logging
import os
import threading
from flask import Flask
from flask import request
from json import loads
from kafka import KafkaConsumer

import send_colis as send_colis

debug_level = os.environ["DEBUG_LEVEL"]

if debug_level == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
elif debug_level == "INFO":
    logging.basicConfig(level=logging.INFO)
elif debug_level == "WARNING":
    logging.basicConfig(level=logging.WARNING)
elif debug_level == "ERROR":
    logging.basicConfig(level=logging.ERROR)
elif debug_level == "CRITICAL":
    logging.basicConfig(level=logging.CRITICAL)

topic_from_tweethon = os.environ["FROM_TWEETHON"]
topic_from_comparathon = os.environ["FROM_COMPARATHON"]
topic_from_travelthon = os.environ["FROM_TRAVELTHON"]

colissithon_port = os.environ["COLISSITHON_PORT"]
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])

app = Flask(__name__)


@app.route('/create_bio', methods=['POST'])
def create_candidate_biographics():
    logging.info('create_bio service called')
    personJson = request.get_json()
    first_name = personJson['biographicsFirstName']
    name = personJson['biographicsName']
    picture = personJson['biographicsImage']
    picture_type = personJson['biographicsImageContentType']
    bio_id = send_colis.create_new_biographics(first_name, name, picture, picture_type)
    return str(bio_id)


@app.route('/bind_bio', methods=['POST'])
def create_related_biographics():
    logging.info('bind_bio service called')
    send_colis.bind_bio_to_bio(request.get_json())


@app.route('/create_minibio', methods=['POST'])
def create_mini_biographics():
    colis_json = request.get_json()
    first_name = colis_json['biographicsFirstName']
    name = colis_json['biographicsName']
    picture = None
    picture_type = None
    bio_id = send_colis.create_new_biographics(first_name, name, picture, picture_type)
    return str(bio_id)


@app.route('/create_location', methods=['POST'])
def create_location():
    colis_json = request.get_json()
    location_name = colis_json['locationName']
    # coordonnées sous la forme "latitude, longitude"
    location_coord = colis_json['locationCoordinates']
    locationType = None
    location_id = send_colis.create_location(location_name, locationType, location_coord)
    return str(location_id)


def start_REST_server(port):
    app.run(host='0.0.0.0', port=port)


def start_travelthon_consummer():
    consumer = KafkaConsumer(
        topic_from_travelthon,
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for travelthon started')
    for msg in consumer:
        logging.debug('Consume message from ##travelthon_out')
        topic_json = msg.value
        bio_id = topic_json['idBio']
        location_json = topic_json['location']
        send_colis.create_location_and_bind(location_json, bio_id)


def start_tweets_consumer():
    consumer = KafkaConsumer(
        topic_from_tweethon,
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for Tweethon started')
    for msg in consumer:
        logging.debug('Consume message from ##tweethon_out')
        tweet_json = msg.value[0]
        bio_id = msg.value[1]
        logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
        # print("bio_id "+bio_id)
        send_colis.link_tweet_to_bio(tweet_json, bio_id)


def start_pictures_consumer():
    consumer = KafkaConsumer(
        topic_from_comparathon,
        bootstrap_servers=[kafka_endpoint],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    logging.info('Kafka Consumer for Comparathon started')
    for msg in consumer:
        logging.debug('Consume message from ##comparathon_out')
        picture_json = msg.value[0]
        bio_id = msg.value[1]
        logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
        # print("bio_id "+bio_id)
        send_colis.link_picture_to_bio(picture_json, bio_id)


if __name__ == '__main__':
    REST_thread = threading.Thread(target=start_REST_server, args=(colissithon_port,))
    rawdatas_thread = threading.Thread(target=start_tweets_consumer)
    pictures_thread = threading.Thread(target=start_pictures_consumer)
    travelthon_thread = threading.Thread(target=start_travelthon_consummer)

    REST_thread.start()
    logging.info('REST Thread started')
    rawdatas_thread.start()
    logging.info('Kafka tweethon_out Thread started')
    pictures_thread.start()
    logging.info('Kafka comparathon_out Thread started')
    travelthon_thread.start()
    logging.info('Kafka travelthon_out Thread started')
