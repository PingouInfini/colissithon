import json
import logging
import threading

from kafka import KafkaConsumer

from src import send_colis
from src import variables

topic_from_tweethon = variables.topic_from_tweethon
topic_from_comparathon_pictures = variables.topic_from_comparathon_pictures
topic_from_travelthon = variables.topic_from_travelthon
topic_from_croustibatch = variables.topic_from_croustibatch
topic_from_comparathon_hit = variables.topic_from_comparathon_hit


colissithon_port = variables.colissithon_port
kafka_endpoint = variables.kafka_endpoint


class pictures_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_comparathon_pictures])
        logging.debug("Consume messages from topic :" + str(topic_from_comparathon_pictures))

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
            global_json = msg.value
            bio_id = global_json["idBio"]
            tweet_json = global_json["tweet"]
            logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
            send_colis.link_tweet_to_bio(tweet_json, bio_id)

        consumer.close()

class media_from_tweet_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_croustibatch])
        logging.debug("Consume messages from topic :" + str(topic_from_croustibatch))
        for msg in consumer:
            global_json = msg.value
            bio_id = global_json["idBio"]
            json_picture = global_json["picture"]
            logging.debug("Media from Tweet associated to bio_Id n° : " + str(bio_id))
            send_colis.link_media_to_bio(json_picture, bio_id)

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


class hit_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_comparathon_hit])
        logging.debug("Consume messages from topic :" + str(topic_from_comparathon_hit))
        for msg in consumer:
            logging.info("New message from topic :" + str(topic_from_comparathon_hit))
            msg = msg.value
            bio_id = msg['biographics'].get('idBio')
            logging.debug("Location associated to bio_Id n° : " + str(bio_id))
            send_colis.create_raw_data_url(msg)

        consumer.close()
