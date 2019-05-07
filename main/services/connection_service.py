import json
import requests

from main.variables import authentication_url, account_url


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
