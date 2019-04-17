import base64
import json
import sys
from pathlib import Path
import time
import os

from geopy import geocoders
# -*- coding: UTF-8 -*-
from colissithon.common import service

from colissithon.items import biographics, relation_bio_data, raw_data

def create_new_biographics(nom, prenom, image):
    current_session, current_header = service.authentification();
    bio = biographics(prenom, nom, image, "image/" + (Path(image).suffix).replace(".", ""))
    bio_id = service.create_dto_biographic(bio, current_session, current_header)
    service.close_connection(current_session)
    return bio_id

def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = service.authentification();
    service.rawdatas_from_tweet(json_tweet, current_session, current_header, 4232)

def link_picture_to_bio(picture_path, id_bio):
    pass





if __name__ == '__main__':

    # Détection de l'extension du fichier image et génération de l'objet biographics
    i_want_to_create_bio = (len(sys.argv) == 4)
    i_want_to_create_rawdata_from_tweets = (len(sys.argv) == 1)
    i_want_to_create_rawdata_from_pictures_dir = (len(sys.argv) ==2)

    print("i_want_to_create_bio : " + str(i_want_to_create_bio))
    print("i_want_to_create_rawdata_from_tweets : " + str(i_want_to_create_rawdata_from_tweets))
    # i_want_to_create_bio = True
    # i_want_to_create_rawdata = False
    if i_want_to_create_bio:
        prenom = sys.argv[1]
        nom = sys.argv[2]
        image = sys.argv[3]
        file_type_point = "image/" + Path(image).suffix
        file_type = (file_type_point.replace(".", ""))
        file_type_point = "image/" + (Path(image).suffix).replace(".", "")
        bio = biographics(prenom, nom, image, file_type)

    # Authentification et récupération session authentifiée + header avec le token de sécurité
    current_session, current_header = authentification()

    # Envoi de la Biographics, et récupération de son External ID
    if i_want_to_create_bio:
        bio_id = create_dto_biographic(bio, current_session, current_header)
        print("bio_id ==> " + bio_id)
    # Envoi de la Rawdata et récupération de son External ID
    elif i_want_to_create_rawdata_from_tweets:

        for file in os.listdir("samples/json"):
            # send_rawDatas(rawdatatest, current_session, current_header, "5cb5a5b3149b3f00010dd1c0")
            rawdatas_from_tweet(os.path.join("samples/json", file), current_session, current_header, 4232)

    elif i_want_to_create_rawdata_from_pictures_dir:
        pictures_dir_path = sys.argv[1]
        rawdatas_from_ggimage(pictures_dir_path, current_session, current_header, 4232)

    # Envoi de l'InsightGraphRelation (relation Biographics-RawData)
    close_connection(current_session)
