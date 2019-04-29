import os
import sys
from pathlib import Path
from main.services import biographics_service as bio_serv, connection_service as con_serv, rawDatas_service as raw_serv
from main.items.biographics import biographics
from main.variables import path_to_tweets_dir, path_to_pictures_dir

# -*- coding: UTF-8 -*-

def create_new_biographics(prenom, nom, image):
    bio = biographics(prenom, nom, image, "image/" + (Path(image).suffix).replace(".", ""))
    current_session, current_header = con_serv.authentification()
    bio_id = bio_serv.create_dto_biographic(bio, current_session, current_header)
    con_serv.close_connection(current_session)
    return bio_id

def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_tweet(json_tweet, id_bio, current_session, current_header)

def link_picture_to_bio(path_to_pictures_dir, file, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_ggimage(path_to_pictures_dir, file, id_bio, current_session, current_header)


if __name__ == '__main__':

    print(sys.argv[1])
    # Détection de l'extension du fichier image et génération de l'objet biographics
    i_want_to_create_bio = (sys.argv[1] == str(1))
    i_want_to_create_rawdata_from_tweets = (sys.argv[1] == str(2))
    i_want_to_create_rawdata_from_pictures_dir = (sys.argv[1] == str(3))

    print("i_want_to_create_bio : " + str(i_want_to_create_bio))
    print("i_want_to_create_rawdata_from_tweets : " + str(i_want_to_create_rawdata_from_tweets))
    print("i_want_to_create_rawdata_from_pictures_dir : " + str(i_want_to_create_rawdata_from_pictures_dir))

    if i_want_to_create_bio:
        prenom = sys.argv[2]
        nom = sys.argv[3]
        image = sys.argv[4]
        bio_id = create_new_biographics(prenom,nom,image)
        print("bio_id ==> " + bio_id)

    elif i_want_to_create_rawdata_from_tweets:
        link_item_to_this_id_bio = sys.argv[2]

        index = 0
        for file in os.listdir(path_to_tweets_dir):
            index += 1
            link_tweet_to_bio(os.path.join(path_to_tweets_dir, file), link_item_to_this_id_bio)
            if index > 10 :
                break

    elif i_want_to_create_rawdata_from_pictures_dir:
        link_item_to_this_id_bio = sys.argv[2]

        for file in os.listdir(path_to_pictures_dir):
            link_picture_to_bio(path_to_pictures_dir, file, link_item_to_this_id_bio)