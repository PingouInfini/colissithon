# colissithon

Utilisation d'arguments (1, 2 ou 3) pour tester:
 1. i_want_to_create_bio
 2. i_want_to_create_rawdata_from_tweets
 3. i_want_to_create_rawdata_from_pictures_dir

exemple:

    python3 colissithon.py <1, 2 ou 3> <arguments> 

##Appels de méthodes de tests:

#### create_new_biographics

    python3 colissithon.py 1 bob jouy samples/LaSardine.jpg
    
#### link_tweet_to_bio
> Link all tweets in "samples/json" to id_bio

    python3 colissithon.py 2 <id_bio>
    
##### link_tweet_to_bio
> Link all tweets in "samples/pictures" to id_bio

    python3 colissithon.py 3 <id_bio>   