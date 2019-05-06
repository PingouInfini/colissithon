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
    first_name = colis_json['biographicsFirstName']
    name = colis_json['biographicsName']
    picture = colis_json['biographicsImage']
    picture_type = colis_json['biographicsImageContentType']
    bio_id = send_colis.create_new_biographics(first_name,name,picture, picture_type)
    print (str(first_name) + " " + str(name) + " bien arrivé dans Insight, son image type est : " + str(picture_type))
    return str(bio_id)


def start_REST_server(port) :
    app.run(host='0.0.0.0', port=port)

def start_tweets_consumer() :
    consumer = KafkaConsumer(
        'tweetopic',
        bootstrap_servers = ['localhost:8092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id = 'my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    for msg in consumer :
        tweet_json = msg.value[0]
        bio_id = msg.value[1]
        send_colis.link_tweet_to_bio(tweet_json, bio_id)

def start_pictures_consumer() :
    consumer = KafkaConsumer(
        'topictures',
        bootstrap_servers = ['localhost:8092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id = 'my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    for msg in consumer :
        picture_json = msg.value[0]
        bio_id = msg.value[1]
        send_colis.link_picture_to_bio(picture_json, bio_id)

if __name__ == '__main__':
    REST_thread = threading.Thread(target = start_REST_server, args=(custom_port,))
    rawdatas_thread = threading.Thread(target= start_tweets_consumer)
    pictures_thread = threading.Thread(target= start_pictures_consumer)

    REST_thread.start()
    rawdatas_thread.start()
    pictures_thread.start()



