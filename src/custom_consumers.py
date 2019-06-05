import json
import logging
import threading

from kafka import KafkaConsumer

from src import send_colis
from src import variables

topic_from_tweethon = variables.topic_from_tweethon
topic_from_comparathon = variables.topic_from_comparathon
topic_from_travelthon = variables.topic_from_travelthon

colissithon_port = variables.colissithon_port
kafka_endpoint = variables.kafka_endpoint


class pictures_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_comparathon])
        logging.debug("Consume messages from topic :" + str(topic_from_comparathon))

        for msg in consumer:
            picture_json = msg.value[0]
            bio_id = msg.value[1]
            logging.debug("Picture associated to bio_Id n° : " + str(bio_id))
            send_colis.link_picture_to_bio(picture_json, bio_id)

        consumer.close()



class tweet_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_tweethon])
        logging.debug("Consume messages from topic :" + str(topic_from_tweethon))
        for msg in consumer:
            tweet_json = msg.value[0]
            bio_id = msg.value[1]
            logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
            send_colis.link_tweet_to_bio(tweet_json, bio_id)

        consumer.close()

class location_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_travelthon])
        logging.debug("Consume messages from topic :" + str(topic_from_travelthon))
        for msg in consumer:
            logging.info("New message from topic :" + str(topic_from_travelthon))
            location_json =msg.value
            bio_id = location_json['idBio']
            location_name = location_json['locationName']
            location_coord = location_json ['locationCoordinates']
            logging.debug("Location associated to bio_Id n° : " + str(bio_id))
            send_colis.create_location_and_bind(bio_id, location_name, location_coord)

        consumer.close()