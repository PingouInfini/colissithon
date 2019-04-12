import base64
import json
import sys
from pathlib import Path

import requests

# -*- coding: UTF-8 -*-
from items import biographics, relation_bio_data, raw_data

SERVEUR_URL = "http://localhost:8080"

authentication_url = SERVEUR_URL + "/api/authentication"
account_url = SERVEUR_URL + "/api/account"
biographics_url = SERVEUR_URL + "/api/biographics/"
rawdata_url = SERVEUR_URL + "/api/raw-data"
relation_url = SERVEUR_URL + "/api/graph/relation"


# prenom = sys.argv[1]
# nom = sys.argv[2]
# image = sys.argv[3]


def authentificate():
    try:
        payload = {
            'j_username': 'admin',
            'j_password': 'admin',
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


def create_biographics(biographics, session, header_with_token):
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

    return post_data_to_insight(bio, session, header_with_token, biographics_url)


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

    target_id = post_data_to_insight(data, session, header_with_token, rawdata_url)
    bind_biographics_to_rawdata(biographics_id, target_id, session, header_with_token)


def bind_biographics_to_rawdata(biographics_external_id, rawData_external_id, session, header):
    link ={ "idJanusSource" :  biographics_external_id,
            "idJanusCible" : rawData_external_id,
            "name" : "Related to",
            "typeSource" : "Biographics",
            "typeCible" : "RawData"}

    post_data_to_insight(link, session, header, relation_url)


def post_data_to_insight(data, session, header, target_url):
    postResponse = session.post(url=target_url, json=data, headers=header)
    if postResponse.status_code == 201:
        data = json.loads(postResponse.content)
        target_id = data["id"]
        print("SUCCESSFUL REQUEST :  " + str(postResponse))
        return target_id
    else:
        print("ERROR during request to " + str(target_url) + " ---- RESPONSE IS :  " + str(postResponse))


def close_connection():
    exit(0)


def rawdatas_from_tweet(json_path, session, header, biographics_id):
    # 1- transform tweet into rawData (condition for presence of picture(s))
    try:
        with open(json_path) as json_file:
            rawdata_from_tweet = raw_data(None,None,None,None,None,None,None)
            json_data = json.load(json_file)
            rawdata_from_tweet.rawDataName = json_data['user']['name'] + " " + json_data['created_at']
            if (json_data == 'source'):
                rawdata_from_tweet.rawDataSourceUri = str(json_data['source'])
                print("4     " + str(json_data['source']))
            rawdata_from_tweet.rawDataSourceType = "TWITTER"
            print("5")
            if not (json_data !=('coordinates')) & (str(json_data['coordinates']) == ''):
                rawdata_from_tweet.rawDataCoordinates = str(json_data['coordinates'])
                print("6    " + str(json_data['coordinates']))
            if (json_data == 'source'):
                rawdata_from_tweet.rawDataContent = str(json_data['text'])
                print("7    " + str(json_data['text']))
            # if not (json_datas['entities']['media'] is None) :
            #     #index = 0
            #     #for media in json_datas['entities']['media']:
            #         #index += 1
            #     media = json_datas['entities']['media'][0]
            #     r = requests.get(media['media_url'], allow_redirects=True)
            #     f = r.read()
            #     b = bytearray(f)
            #     decode = base64.b64encode(b).decode('UTF-8')
            #     rawdata_from_tweet.rawDataData = str(decode)
            #     rawdata_from_tweet.rawDataDataContentType = "image/jpg"
            #     #image = r.content
            #     #todo: a bytifier + extension + ajout raw data
                  #todo: trouver comment vérifier l'existence d'une donnée si non obligatoire

        send_rawDatas(rawdata_from_tweet, session, header, biographics_id)

    except:
        raise ValueError ("PROBLEM DURING TWEET DATA'S EXTRACTION")


if __name__ == '__main__':
    # Détection de l'extension du fichier image et génération de l'objet biographics
    #file_type_point = "image/" + Path(image).suffix
    #file_type = (file_type_point.replace(".", ""))
    # file_type_point = "image/" + (Path(image).suffix).replace(".", "")
    #bio = biographics(prenom, nom, image, file_type)
    #rawdatatest = raw_data("Prenom", None, None, None, "THIS IS THE CONTENT TEXT", "Source TEST", None)
    # Authentification et récupération session authentifiée + header avec le token de sécurité
    current_session, current_header = authentificate()

    # Envoi de la Biographics, et récupération de son External ID
    #bio_id = create_biographics(bio, current_session, current_header)

    #send_rawDatas(rawdatatest, current_session, current_header, "5caf0623828d2838988fb174")
    rawdatas_from_tweet("C:/Workspace/colissithon/samples/json/1093211639300743169.json", current_session, current_header, "12344555555")
    #print(str(file_type))

    # Envoi de la Rawdata et récupération de son External ID

    # Envoi de l'InsightGraphRelation (relation Biographics-RawData)


    close_connection()
