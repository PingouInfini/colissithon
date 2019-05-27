import os

# URL
INSIGHT_URL = "http://"+str(os.environ["INSIGHT_IP"])+":"+str(os.environ["INSIGHT_PORT"])
authentication_url = INSIGHT_URL + "/api/authentication"
account_url = INSIGHT_URL + "/api/account"
biographics_url = INSIGHT_URL + "/api/biographics/"
location_url = INSIGHT_URL + "/api/locations/"
rawdata_url = INSIGHT_URL + "/api/raw-data"
relation_url = INSIGHT_URL + "/api/graph/relation"

