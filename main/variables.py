from eat_and_dispatch import param as parameters

# URL
SERVEUR_URL = parameters["insight_url"]
authentication_url = SERVEUR_URL + "/api/authentication"
account_url = SERVEUR_URL + "/api/account"
biographics_url = SERVEUR_URL + "/api/biographics/"
rawdata_url = SERVEUR_URL + "/api/raw-data"
relation_url = SERVEUR_URL + "/api/graph/relation"

# Paths to datas
path_to_tweets_dir = parameters["tweets_directory"]
path_to_pictures_dir = parameters["pictures_directory"]
