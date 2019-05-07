from main.items.biographics import biographics
from main.services import biographics_service as bio_serv, connection_service as con_serv, rawDatas_service as raw_serv


# -*- coding: UTF-8 -*-

def create_new_biographics(prenom, nom, image, image_type):
    bio = biographics(prenom, nom, image, image_type)
    current_session, current_header = con_serv.authentification()
    bio_id = bio_serv.create_dto_biographic(bio, current_session, current_header)
    con_serv.close_connection(current_session)
    return bio_id

def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_tweet(json_tweet, id_bio, current_session, current_header)

def link_picture_to_bio(json_picture, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_ggimage(json_picture, id_bio, current_session, current_header)
