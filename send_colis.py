from src.items.biographics import biographics
from src.services import biographics_service as bio_serv, connection_service as con_serv, rawDatas_service as raw_serv, \
    relation_service as rel_serv


# -*- coding: UTF-8 -*-

def create_new_biographics(first_name, name, picture, picture_type):
    bio = biographics(first_name, name, picture, picture_type)
    current_session, current_header = con_serv.authentification()
    bio_id = bio_serv.create_dto_biographic(bio, current_session, current_header)
    con_serv.close_connection(current_session)
    return bio_id


def bind_bio_to_bio(twoBioIdsJson):
    candidate_bioId = twoBioIdsJson['candidateBioId']
    bioId_to_bind = twoBioIdsJson['relationBioId']
    current_session, current_header = con_serv.authentification()
    rel_serv.bind_object_to_biographics(candidate_bioId, bioId_to_bind, current_session, current_header)


def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_tweet(json_tweet, id_bio, current_session, current_header)


def link_picture_to_bio(json_picture, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_ggimage(json_picture, id_bio, current_session, current_header)
