from io import BytesIO

import requests
import logging

if __name__ == '__main__':

    accountUrl = "http://localhost:8080/api/account"
    authenticationUrl = "http://localhost:8080/api/authentication"
    # url = "http://localhost:8080/api/raw-data/5c48cf9969f04e27882e32a7"
    url = "http://localhost:8080/api/raw-data"
    payload = {
        'j_username': "admin",
        'j_password': "admin",
        'remember-me': 'true',
        'submit': 'Login'
    }
    with requests.Session() as session:
        myResponse = session.get(accountUrl, verify=True)
        if myResponse.status_code == 401:
            token = session.cookies.get("XSRF-TOKEN")
            headers = {
                'Accept': 'application/json',
                'Connection': 'keep-alive',
                'X-XSRF-TOKEN': token,
            }
            authResponse = session.post(url=authenticationUrl, data=payload, verify=True, headers=headers)
            if authResponse.ok:
                logging.debug("Authenticated")
                # request to insight
                headersRawData = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-type': 'application/json',
                    'X-XSRF-TOKEN': authResponse.cookies.get("XSRF-TOKEN")
                }

                rawData = {
                    "rawDataName": "prout",
                    "rawDataCreationDate": "1569502656.9615667",
                    "rawDataSubType": "url",
                    "rawDataContent": str({
                        "nom": "Macron",
                        "prenom": "Emmanuel",
                        "idBio": "4168"
                    }),
                    "rawDataSourceUri": "https://www.dna.fr/edition-de-strasbourg/2019/09/25/visite-de-macron-a"
                                        "-strasbourg-un-hommage-aux-heros-de-l-attentat",
                    "scoreDTO": {
                        "points": 10,
                        "listThemeMotclefHit": [
                            "TER.jazz", "ESP.rap"
                        ],
                        "imageHit": 0,
                        "frequence": 0}


                }

                basic_post_response = session.post(url=url, json=rawData, headers=headersRawData)

                if basic_post_response.ok:
                    print("")
                    # os.remove(imagefilename)
                else:
                    # If response code is not ok (200), print the resulting http error code with description
                    basic_post_response.raise_for_status()

