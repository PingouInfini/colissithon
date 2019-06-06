import base64
import json
import time

import requests

from src.items.raw_data import raw_data
from src.services import relation_service
from src.variables import rawdata_url

resolved_locations = {}


def rawdatas_from_ggimage(json_picture, biographics_id, session, header):
    # Extract picture and metadatas from json and prepare bio-img rawdata
    rawdata_from_picture = raw_data(None, None, None, None, None, None, None, None, str(time.time()))
    rawdata_from_picture.rawDataName = json_picture['name']
    rawdata_from_picture.rawDataSubType = "bio-img" # permet l'affichage dans le panel gg img de l'idcard d'insight
    rawdata_from_picture.rawDataSourceUri = "Google Images"
    rawdata_from_picture.rawDataDataContentType = json_picture['extension']
    rawdata_from_picture.rawDataData = json_picture['image']
    send_rawDatas(rawdata_from_picture, biographics_id, session, header)

def rawdatas_from_media(json_picture, biographics_id, session, header) :
    # Extract picture and metadatas from json and prepare media-img rawdata
    rawdata_from_picture = raw_data(None, None, None, None, None, None, None, None, str(time.time()))
    rawdata_from_picture.rawDataName = json_picture['name']
    rawdata_from_picture.rawDataSubType = "media-img" # permet l'affichage dans le panel media de l'idcard d'insight
    rawdata_from_picture.rawDataSourceUri = "Twitter Account"
    rawdata_from_picture.rawDataDataContentType = json_picture['extension']
    rawdata_from_picture.rawDataData = json_picture['image']
    send_rawDatas(rawdata_from_picture, biographics_id, session, header)

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

        send_rawDatas(rawdata_from_tweet, biographics_id, session, header)

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


def send_rawDatas(rawData, biographics_id, session, header_with_token):
    data = {
        "rawDataName": rawData.rawDataName,
    }
    if not (rawData.rawDataCoordinates is None):
        data.update({"rawDataCoordinates": rawData.rawDataCoordinates})

    if not (rawData.rawDataContent is None):
        data.update({"rawDataContent": rawData.rawDataContent})

    if not (rawData.rawDataSourceType is None):
        data.update({"rawDataSourceType": rawData.rawDataSourceType})

    if not (rawData.rawDataSourceUri is None):
        data.update({"rawDataSourceUri": rawData.rawDataSourceUri})

    if not (rawData.rawDataData is None):
        data.update({"rawDataData": rawData.rawDataData,
                     "rawDataDataContentType": rawData.rawDataDataContentType})

    if not (rawData.rawDataSubType is None):
        data.update({"rawDataSubType": rawData.rawDataSubType})

    if not (rawData.rawDataCreationDate is None):
        data.update({"rawDataCreationDate": rawData.rawDataCreationDate})

    post_response = session.post(url=rawdata_url, json=data, headers=header_with_token)

    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        relation_service.bind_object_to_biographics(biographics_id, target_ID, session, header_with_token)
        return target_ID
