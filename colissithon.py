import sys
from pathlib import Path
import os

from geopy import geocoders
# -*- coding: UTF-8 -*-

import common.services as services
from items import biographics

def create_new_biographics(nom, prenom, image):
    bio = biographics(prenom, nom, image, "image/" + (Path(image).suffix).replace(".", ""))
    current_session, current_header = services.authentification();
    bio_id = services.create_dto_biographic(bio, current_session, current_header)
    services.close_connection(current_session)
    return bio_id

def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = services.authentification();
    services.rawdatas_from_tweet(json_tweet, id_bio, current_session, current_header)

def link_picture_to_bio(picture_path, id_bio):
    pass


if __name__ == '__main__':

    print(sys.argv[1])
    # Détection de l'extension du fichier image et génération de l'objet biographics
    i_want_to_create_bio = (sys.argv[1] == str(1))
    i_want_to_create_rawdata_from_tweets = (sys.argv[1] == str(2))
    i_want_to_create_rawdata_from_pictures_dir = (sys.argv[1] == str(3))

    print("i_want_to_create_bio : " + str(i_want_to_create_bio))
    print("i_want_to_create_rawdata_from_tweets : " + str(i_want_to_create_rawdata_from_tweets))
    print("i_want_to_create_rawdata_from_pictures_dir : " + str(i_want_to_create_rawdata_from_pictures_dir))

    # i_want_to_create_bio = True
    # i_want_to_create_rawdata = False
    if i_want_to_create_bio:
        prenom = sys.argv[2]
        nom = sys.argv[3]
        image = sys.argv[4]
        bio_id = create_new_biographics(prenom,nom,image)
        print("bio_id ==> " + bio_id)

    elif i_want_to_create_rawdata_from_tweets:
        link_item_to_this_id_bio = sys.argv[2]

        for file in os.listdir("samples/json"):
            link_tweet_to_bio(os.path.join("samples/json", file), link_item_to_this_id_bio)

    elif i_want_to_create_rawdata_from_pictures_dir:
        link_item_to_this_id_bio = sys.argv[2]

        #TODO FIXME ne fonctionne pas en l'état
        for file in os.listdir("samples/pictures"):
            link_tweet_to_bio(os.path.join("samples/pictures", file), link_item_to_this_id_bio)