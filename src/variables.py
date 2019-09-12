import os

# SERVEUR INSIGHT

# INSIGHT_URL = "http://" + str(os.environ["INSIGHT_IP"]) + ":" + str(os.environ["INSIGHT_PORT"])
INSIGHT_URL = "http://" + "192.168.0.9" + ":" + "8080"

authentication_url = INSIGHT_URL + "/api/authentication"
account_url = INSIGHT_URL + "/api/account"
biographics_url = INSIGHT_URL + "/api/biographics/"
location_url = INSIGHT_URL + "/api/locations/"
rawdata_url = INSIGHT_URL + "/api/raw-data"
search_rawdata_url = INSIGHT_URL + "/api/_search/raw-data"
relation_url = INSIGHT_URL + "/api/graph/relation"
dictionary_url = INSIGHT_URL + "/api/dictionary/"


# KAFKA
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])
# kafka_endpoint = "192.168.0.9" + ":" + "8092"




# topic_from_comparathon_pictures = os.environ["FROM_COMPARATHON_PICTURES"]
# topic_from_comparathon_hit = os.environ["FROM_COMPARATHON_HIT"]

topic_from_comparathon_pictures = "ggimgToColissi"
topic_from_comparathon_hit = "comparaToColissi"


topic_from_tweethon = "tweetToColissi"
topic_from_travelthon = "locToColissi"
topic_from_croustibatch = "tweetToCrousti"



#
# # topic d'envoi de rawdata vers Coli puis Reach



# COLISSITHON
colissithon_port = os.environ["COLISSITHON_PORT"]
# colissithon_port = "9876"

# LOGS LEVEL
debug_level = os.environ["DEBUG_LEVEL"]
# debug_level = "INFO"

