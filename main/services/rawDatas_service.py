import requests
import os
import base64
from main.items.raw_data import raw_data
import json
from pathlib import Path
import time
from main.variables import relation_url
from main.variables import rawdata_url

resolved_locations = {}


def rawdatas_from_ggimage(path_to_pictures_dir,file, biographics_id, session, header):
    # for picture in os.listdir(dir_path):
    fname, fext = os.path.splitext(file)
    file_type_point = "image/" + str(fext).replace(".", "")
    print("####################################   " + file_type_point)

    rawdata_from_picture = raw_data(None, None, None, None, None, None, None, str(time.time()))
    with open(path_to_pictures_dir + "/" + file, "rb") as image:
        f = image.read()
        b = bytearray(f)
        decode = base64.b64encode(b).decode('UTF-8')
        rawdata_from_picture.rawDataName = str(file)
        rawdata_from_picture.rawDataSourceUri = "Google Images"
        rawdata_from_picture.rawDataSourceType = "TWITTER"
        rawdata_from_picture.rawDataDataContentType = file_type_point
        rawdata_from_picture.rawDataData = str(decode)
    send_rawDatas(rawdata_from_picture, biographics_id, session, header)


def rawdatas_from_tweet(json_path, biographics_id, session, header):
    # 1- transform tweet into rawData (condition for presence of picture(s))
    try:
        with open(json_path) as json_file:
            rawdata_from_tweet = raw_data(None, None, None, None, None, None, None, str(time.time()))
            json_data = json.load(json_file)
            rawdata_from_tweet.rawDataName = json_data['user']['name'] + " " + json_data['created_at']
            rawdata_from_tweet.rawDataSourceUri = json_data['source']
            rawdata_from_tweet.rawDataSourceType = "TWITTER"
            try:
                rawdata_from_tweet.rawDataCoordinates = extract_coord_from_tweet(json_data)
            except:
                pass
            try:
                rawdata_from_tweet.rawDataContent = json_data['text']
            except:
                pass
            try:
                index = 0
                first_media = json_data['entities']['media'][0]
                print(first_media['media_url'])
                r = requests.get(first_media['media_url'], allow_redirects=True)
                if (first_media['type'] == "photo"):
                    rawdata_from_tweet.rawDataDataContentType = "image/jpg"
                    decode = base64.b64encode(r.content).decode('UTF-8')
                    rawdata_from_tweet.rawDataData = str(decode)
            except:
                pass
        print("###### SERVICE POSTAL")

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

    if not (rawData.rawDataCreationDate is None):
        data.update({"rawDataCreationDate": rawData.rawDataCreationDate})

    post_response = session.post(url = rawdata_url, json = data, headers = header_with_token)

    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF RAWDATA IS :" + str(target_ID))
        bind_biographics_to_rawdata(biographics_id, target_ID, session, header_with_token)
        return target_ID

def bind_biographics_to_rawdata (biographics_id, target_ID, session, header_with_token) :
    link = {"idJanusSource" : biographics_id,
            "idJanusCible" : target_ID,
            "typeSource" : "Biographics",
            "typeCible" : "RawData"}
    post_response = session.post(url = relation_url, json = link, headers = header_with_token)
    print (str(post_response) + "   : liens bio-rawdatas bien créé")