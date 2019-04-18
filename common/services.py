import requests
import json
import base64
import time

from items import raw_data

# SERVEUR_URL = "http://172.20.0.8:8080"
SERVEUR_URL = "http://localhost:8080"

authentication_url = SERVEUR_URL + "/api/authentication"
account_url = SERVEUR_URL + "/api/account"
biographics_url = SERVEUR_URL + "/api/biographics/"
rawdata_url = SERVEUR_URL + "/api/raw-data"
relation_url = SERVEUR_URL + "/api/graph/relation"

resolved_locations = {}

def authentification(username="admin", password="admin"):
    try:
        payload = {
            'j_username': username,
            'j_password': password,
            'remember-me': 'true',
            'submit': 'Login'
        }
        session = requests.Session()
        myResponse = session.get(account_url, verify=True)
        if myResponse.status_code == 401:
            token = session.cookies.get("XSRF-TOKEN")
            headers = {
                'Accept': 'application/json',
                'Connection': 'keep-alive',
                'X-XSRF-TOKEN': token
            }
            authResponse = session.post(url=authentication_url, data=payload, verify=True, headers=headers)

            if authResponse.ok:
                headersRawData = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-type': 'application/json',
                    'X-XSRF-TOKEN': authResponse.cookies.get("XSRF-TOKEN")
                }

                return (session, headersRawData)

            else:
                print("Auth failed")
        else:  # For successful API call, response code will be 200 (OK)
            if myResponse.ok:
                jData = json.loads(myResponse.content)
                print("The response contains {0} properties".format(len(jData)))
                print("\n")
                for key in jData:
                    print(key + " : " + jData[key])
            else:
                # If response code is not ok (200), print the resulting http error code with description
                myResponse.raise_for_status()

    except:
        raise ValueError("Authorization failed")

def close_connection(current_session):
    current_session.close()
    # exit(0)

def create_dto_biographic(biographics, session, header_with_token):
    with open(biographics.biographicsImage, "rb") as image:
        f = image.read()
        b = bytearray(f)
        decode = base64.b64encode(b).decode('UTF-8')

    bio = {
        "biographicsFirstname": biographics.biographicsFirstname,
        "biographicsName": biographics.biographicsName,
        "biographicsImageContentType": biographics.biographicsImageContentType,
        "biographicsImage": str(decode)
    }

    post_response = post_data_to_insight(bio, session, header_with_token, biographics_url)
    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF BIOGRAPHICS IS :" + str(target_ID))
        return target_ID

def send_rawDatas(rawData, session, header_with_token, biographics_id):
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

    post_response = post_data_to_insight(data, session, header_with_token, rawdata_url)

    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF RAWDATA IS :" + str(target_ID))
        bind_biographics_to_rawdata(biographics_id, target_ID, session, header_with_token)
        return target_ID


def bind_biographics_to_rawdata(biographics_external_id, rawData_external_id, session, header):
    link = {"idJanusSource": biographics_external_id,
            "idJanusCible": rawData_external_id,
            "name": "Related to",
            "typeSource": "Biographics",
            "typeCible": "RawData"}

    post_response = post_data_to_insight(link, session, header, relation_url)
    if post_response.status_code == 201:
        print("Biographics et Rawdata liés")


def post_data_to_insight(data, session, header, target_url):
    post_response = session.post(url=target_url, json=data, headers=header)
    return post_response


def rawdatas_from_ggimage(dir_path, session, header, biographics_id):
    for picture in os.listdir(dir_path):
        file_type_point = "image/" + (Path(picture).suffix).replace(".", "")
        rawdata_from_picture = raw_data(None, None, None, None, None, None, None, str(time.time()))
        with open(dir_path + "/" + picture, "rb") as image:
            f = image.read()
            b = bytearray(f)
            decode = base64.b64encode(b).decode('UTF-8')
            rawdata_from_picture.rawDataName = str(picture)
            rawdata_from_picture.rawDataSourceUri = "Google Images"
            rawdata_from_picture.rawDataSourceType = "TWITTER"
            rawdata_from_picture.rawDataDataContentType = file_type_point
            rawdata_from_picture.rawDataData = str(decode)
        send_rawDatas(rawdata_from_picture, session, header, biographics_id)


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
        print ("###### SERVICE POSTAL")
        send_rawDatas(rawdata_from_tweet, session, header, biographics_id)

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
