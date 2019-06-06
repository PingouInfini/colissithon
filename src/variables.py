import os

# SERVEUR INSIGHT
INSIGHT_URL = "http://" + str(os.environ["INSIGHT_IP"]) + ":" + str(os.environ["INSIGHT_PORT"])
authentication_url = INSIGHT_URL + "/api/authentication"
account_url = INSIGHT_URL + "/api/account"
biographics_url = INSIGHT_URL + "/api/biographics/"
location_url = INSIGHT_URL + "/api/locations/"
rawdata_url = INSIGHT_URL + "/api/raw-data"
relation_url = INSIGHT_URL + "/api/graph/relation"

# KAFKA
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])
topic_from_tweethon = os.environ["FROM_TWEETHON"]
topic_from_comparathon = os.environ["FROM_COMPARATHON"]
topic_from_travelthon = os.environ["FROM_TRAVELTHON"]
topic_from_croustibatch = os.environ["FROM_CROUSTIBATCH"]

# COLISSITHON
colissithon_port = os.environ["COLISSITHON_PORT"]

# LOGS LEVEL
debug_level = os.environ["DEBUG_LEVEL"]
