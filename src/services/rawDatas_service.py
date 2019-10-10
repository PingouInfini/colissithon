import base64
import json
import time
import uuid

import requests

from src.Entities import Entities
from src.items.raw_data import raw_data
from src.services import relation_service
from src.variables import rawdata_url, search_rawdata_url

resolved_locations = {}


def rawdatas_from_ggimage(json_picture, biographics_id, rawdata_url_name, session, header):
    # Extract picture and metadatas from json and prepare bio-img rawdata
    rawdata_from_picture = raw_data(None, None, None, None, None, None, None, None, str(time.time()))
    rawdata_from_picture.rawDataName = json_picture['name']
    rawdata_from_picture.rawDataSubType = "bio-img"  # permet l'affichage dans le panel gg img de l'idcard d'insight
    rawdata_from_picture.rawDataSourceUri = "Google Images"
    rawdata_from_picture.rawDataDataContentType = json_picture['extension']
    rawdata_from_picture.rawDataData = json_picture['image']
    rawdata_from_picture.rawDataContent = rawdata_url_name
    create_rawdata_and_link_to_entity(rawdata_from_picture, rawdata_url_name, Entities.Rawdata, Entities.Rawdata,
                                      session, header)


def rawdatas_from_media(json_picture, biographics_id, session, header):
    # Extract picture and metadatas from json and prepare media-img rawdata
    rawdata_from_picture = raw_data(None, None, None, None, None, None, None, None, str(time.time()))
    rawdata_from_picture.rawDataName = json_picture['name']
    rawdata_from_picture.rawDataSubType = "media-img"  # permet l'affichage dans le panel media de l'idcard d'insight
    rawdata_from_picture.rawDataSourceUri = "Twitter Account"
    rawdata_from_picture.rawDataDataContentType = json_picture['extension']
    rawdata_from_picture.rawDataData = json_picture['image']
    create_rawdata_and_link_to_entity(rawdata_from_picture, biographics_id, Entities.Rawdata, Entities.Biographics,
                                      session, header)


def rawdatas_from_url(msg, session, header):
    # Extract metadatas from hit
    rawdata_from_url = raw_data(None, None, None, None, None, None, None, None, str(time.time()))
    rawdata_from_url.rawDataName = msg[1]  # rawdata_url_name
    rawdata_from_url.rawDataSubType = "url"
    rawdata_from_url.rawDataContent = str(msg[2])  # msg
    # rawdata_from_picture.rawDataDataContentType = json_picture['extension']
    # rawdata_from_picture.rawDataData = json_picture['image']
    # rawdata_from_picture.rawDataContent
    bio_id = msg[0]
    create_rawdata_and_link_to_entity(rawdata_from_url, bio_id, Entities.Rawdata, Entities.Biographics, session, header)
    find_unlinked_rawdata_from_gg_image(msg[1], msg[0], Entities.Rawdata, Entities.Rawdata, session, header)


def rawdatas_from_tweet(json_tweet, biographics_id, session, header):
    # 1- transform tweet into rawData (condition for presence of picture(s))
    try:
        rawdata_from_tweet = raw_data(None, None, None, None, None, None, None, None, str(time.time()))
        rawdata_from_tweet.rawDataName = json_tweet['user']['name'] + " " + json_tweet['created_at']
        rawdata_from_tweet.rawDataSourceUri = json_tweet['source']
        rawdata_from_tweet.rawDataSourceType = "TWITTER"
        try:
            rawdata_from_tweet.rawDataCoordinates = extract_coord_from_tweet(json_tweet)
        except:
            pass
        try:
            rawdata_from_tweet.rawDataContent = json_tweet['text']
        except:
            pass
        try:
            index = 0
            first_media = json_tweet['entities']['media'][0]
            r = requests.get(first_media['media_url'], allow_redirects=True)
            if (first_media['type'] == "photo"):
                rawdata_from_tweet.rawDataDataContentType = "image/jpg"
                decode = base64.b64encode(r.content).decode('UTF-8')
                rawdata_from_tweet.rawDataData = str(decode)
        except:
            pass

        create_rawdata_and_link_to_entity(rawdata_from_tweet, biographics_id, Entities.Rawdata, Entities.Biographics,
                                          session, header)

    except:
        raise ValueError("PROBLEM DURING TWEET DATA'S EXTRACTION")


def extract_coord_from_tweet(tweet):
    if tweet['coordinates'] is not None:
        lng = tweet['coordinates']['coordinates'][0]
        lat = tweet['coordinates']['coordinates'][1]
    elif tweet['place'] is not None:
        # relevance-based search by location and name
        (lat, lng) = geodecode(tweet['place']['full_name'])
        if lat == 0 and lng == 0:
            # relevance-based search by different location and name values
            (lat, lng) = geodecode(tweet['contributors'], ['coordinates'])
            if lat == 0 and lng == 0:
                pass

    return str(lat) + ',' + str(lng)


def geodecode(location):
    # check if location already resolved
    if location in resolved_locations:
        loc = resolved_locations.get(location, "none")
    else:
        g = geocoders.Nominatim(user_agent="dummy")
        loc = g.geocode(location, timeout=10)
        # store location and coord
        resolved_locations[location] = loc

    return loc.latitude, loc.longitude


def create_rawDatas(rawData, session, header_with_token):
    data = {
        "rawDataName": rawData.rawDataName,
    }
    if not (rawData.rawDataCoordinates is None):
        data.update({"rawDataCoordinates": rawData.rawDataCoordinates})

    if not (rawData.rawDataSourceType is None):
        data.update({"rawDataSourceType": rawData.rawDataSourceType})

    if not (rawData.rawDataData is None):
        data.update({"rawDataData": rawData.rawDataData,
                     "rawDataDataContentType": rawData.rawDataDataContentType})

    if not (rawData.rawDataCreationDate is None):
        data.update({"rawDataCreationDate": rawData.rawDataCreationDate})

    if not (rawData.rawDataSubType is None):
        data.update({"rawDataSubType": rawData.rawDataSubType})

        if rawData.rawDataSubType == "url":

            biographicsData = json.loads(rawData.rawDataContent.replace("\'", "\""))["biographics"]
            urlsResults = json.loads(rawData.rawDataContent.replace("\'", "\""))["urlsResults"]
            
            if not (rawData.rawDataContent is None):
                data.update({"rawDataContent": str(biographicsData)})
            data.update({"rawDataSourceUri": urlsResults["url"]})
            data.update({"scoreDTO": {
                "points": urlsResults["points"],
                "listThemeMotclefHit": urlsResults["listThemeMotclefHit"],
                "imageHit": urlsResults["imageHit"],
                "frequence": urlsResults["frequence"],
                "depthLevel": urlsResults["depthLevel"],
                "idDictionary": urlsResults["idDictionary"]
            }})
    else:
        if not (rawData.rawDataSourceUri is None):
            data.update({"rawDataSourceUri": rawData.rawDataSourceUri})

        if not (rawData.rawDataContent is None):
            data.update({"rawDataContent": rawData.rawDataContent})

    post_response = session.post(url=rawdata_url, json=data, headers=header_with_token)

    return post_response


def create_rawdata_and_link_to_entity(rawdata_to_create_id, entity_target, type_source, type_cible, session,
                                      header_with_token):
    get_rawdata_response = ''
    post_response_create_rawdata = create_rawDatas(rawdata_to_create_id, session, header_with_token)
    if type_cible == Entities.Rawdata:
        url_get_rawdata_by_dataname = search_rawdata_url + "?page=-1&query=" + entity_target + "&size=20&sort=id,asc"
        get_rawdata_response = session.get(url=url_get_rawdata_by_dataname, headers=header_with_token)
    if post_response_create_rawdata.status_code == 201 or get_rawdata_response.status_code == 200:
        if get_rawdata_response:
            try:
                if get_rawdata_response.content:
                    entity_target = json.loads((get_rawdata_response.content).decode("utf-8"))[0]["externalId"]
            except Exception as e:
                print("rawdataURL pas encore cree", e)
        data = json.loads(post_response_create_rawdata.content)
        rawdata_created_external_id = data["externalId"]
        relation_service.bind_object_to_object(entity_target, rawdata_created_external_id, type_source, type_cible,
                                               session, header_with_token)

        return rawdata_created_external_id


def find_unlinked_rawdata_from_gg_image(rawdata_url_name, rawdata_url_id, type_source, type_cible, session,
                                        header_with_token):
    # url_get_rawdata_by_dataname = search_rawdata_url +"?page=0&query="+rawdata_url_name+"&size=20&sort=id,asc"
    # get_rawdata_response = session.get(url=url_get_rawdata_by_dataname, headers=header_with_token)
    # data = json.loads(get_rawdata_response.content)
    # for rawdata in data:
    #     if rawdata["rawDataContent"] == rawdata_url_name:
    #         relation_service.bind_object_to_object(rawdata_url_id, rawdata["externalId"],  type_source, type_cible,
    #                                                session, header_with_token)
    return True
