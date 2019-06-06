import logging
from src.items.biographics import biographics
from src.items.location import location
from src.services import biographics_service as bio_serv, connection_service as con_serv, rawDatas_service as raw_serv, \
    relation_service as rel_serv, location_service as location_serv


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


def bind_idbio_to_idbio(candidate_bioId, bioId_to_bind):
    current_session, current_header = con_serv.authentification()
    rel_serv.bind_object_to_biographics(candidate_bioId, bioId_to_bind, current_session, current_header)


def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_tweet(json_tweet, id_bio, current_session, current_header)


def link_media_to_bio(json_picture, bio_id):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_media(json_picture, bio_id, current_session, current_header)


def link_picture_to_bio(json_picture, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_ggimage(json_picture, id_bio, current_session, current_header)


def create_location(locationName, locationType, locationCoordinates):
    loc = location(locationName, locationType, locationCoordinates)
    current_session, current_header = con_serv.authentification()
    location_id = location_serv.create_dto_location(loc, current_session, current_header)
    con_serv.close_connection(current_session)
    return location_id


def create_location_and_bind(bio_id, location_name, location_coord):
    locationType = None
    location_id = create_location(location_name, locationType, location_coord)
    bind_idbio_to_idbio(bio_id, location_id)
