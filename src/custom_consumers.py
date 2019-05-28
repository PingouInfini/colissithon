import logging
import threading
import json

from kafka import KafkaConsumer

from src import send_colis

topic_from_tweethon = os.environ["FROM_TWEETHON"]
topic_from_comparathon = os.environ["FROM_COMPARATHON"]
topic_from_travelthon = os.environ["FROM_TRAVELTHON"]

colissithon_port = os.environ["COLISSITHON_PORT"]
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])#

class pictures_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_comparathon])
        logging.debug("Consume messages from topic :"+str(topic_from_comparathon))
        for msg in consumer:

            picture_json = msg.value[0]
            bio_id = msg.value[1]
            logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
            send_colis.link_picture_to_bio(picture_json, bio_id)

        consumer.close()


class tweet_consumer(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')

        consumer.subscribe([topic_from_tweethon])
        logging.debug("Consume messages from topic :"+str(topic_from_tweethon))
        for msg in consumer:
            tweet_json = msg.value[0]
            bio_id = msg.value[1]
            logging.debug("Tweet associated to bio_Id n° : " + str(bio_id))
            send_colis.link_tweet_to_bio(tweet_json, bio_id)

        consumer.close()
