import logging
from src.items.biographics import biographics
from src.items.location import location
from src.services import biographics_service as bio_serv, connection_service as con_serv, rawDatas_service as raw_serv, \
    relation_service as rel_serv, location_service as location_serv
import json
from .Entities import Entities


# -*- coding: UTF-8 -*-

def create_new_biographics(first_name, name, picture, picture_type):
    bio = biographics(first_name, name, picture, picture_type)
    current_session, current_header = con_serv.authentification()
    bio_id = bio_serv.create_dto_biographic(bio, current_session, current_header)
    con_serv.close_connection(current_session)
    return bio_id


def bind_bio_to_bio(twoBioIdsJson):
    bind_idbio_to_idbio(twoBioIdsJson['candidateBioId'], twoBioIdsJson['relationBioId'])


def bind_idbio_to_idbio(candidate_bioId, bioId_to_bind):
    current_session, current_header = con_serv.authentification()
    rel_serv.bind_object_to_object(candidate_bioId, bioId_to_bind, Entities.Biographics, Entities.Rawdata, current_session, current_header)


def link_tweet_to_bio(json_tweet, id_bio):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_tweet(json_tweet, id_bio, current_session, current_header)


def link_media_to_bio(json_picture, bio_id):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_media(json_picture, bio_id, current_session, current_header)


def link_picture_to_bio(json_picture, id_bio, rawdata_url_name):
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_ggimage(json_picture, id_bio, rawdata_url_name, current_session, current_header)


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


def get_dico():
    # tab=[
    #     {'sport': [{'rugby':'3'}, {'football':'8'}, {'tennis':'6'}]},
    #     {'musique': [{'jazz':'2'}, {'rap':'8'}, {'rock':'4'}]}
    # ]

    tab = {
        "theme": [
            {
                "name": "terrorisme",
                "motclef":
                    [
                        {
                            "clef": "rugby",
                            "pond": "3"
                        },
                        {
                            "clef": "football",
                            "pond": "8"
                        },
                        {
                            "clef": "tennis",
                            "pond": "6"
                        }
                    ]
            },
            {
                "name": "espionnage",
                "motclef":
                    [
                        {
                            "clef": "jazz",
                            "pond": "2"
                        },
                        {
                            "clef": "rap",
                            "pond": "7"
                        },
                        {
                            "clef": "rock",
                            "pond": "4"
                        }
                    ]
            },
            {
                "name": "sabotage",
                "motclef":
                    [
                        {
                            "clef": "baroque",
                            "pond": "1"
                        },
                        {
                            "clef": "graffiti",
                            "pond": "10"
                        }
                    ]
            },
            {
                "name": "subversion",
                "motclef":
                    [
                        {
                            "clef": "histoire",
                            "pond": "10"
                        },
                        {
                            "clef": "géographie",
                            "pond": "4"
                        }
                    ]
            },
            {
                "name": "crime organisé",
                "motclef":
                    [
                        {
                            "clef": "chien",
                            "pond": "8"
                        },
                        {
                            "clef": "chat",
                            "pond": "4"
                        }
                    ]
            }
        ]
    }
    jsonTab = json.dumps(tab)
    return jsonTab


def create_raw_data_url (msg):
    # check si le rawdata existe, créer ou mettre à jour envoyer à Coli le rawdata
    current_session, current_header = con_serv.authentification()
    raw_serv.rawdatas_from_url(msg, current_session, current_header)


