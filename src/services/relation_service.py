from src.Entities import Entities
from src.variables import relation_url


def bind_object_to_object(idJanusSource, idJanusCible, typeSource: Entities, typeCible: Entities, session,
                          header_with_token):
    link = {"idJanusSource": idJanusSource,
            "idJanusCible": idJanusCible,
            "typeSource": typeSource.name,
            "typeCible": typeCible.name,
            "name": "linkedTo"}
    post_response = session.post(url=relation_url, json=link, headers=header_with_token)
    if post_response.status_code == 201:
        print("SUCCESSFUL REQUEST :  " + str(post_response))
    link = {"idJanusSource": idJanusCible,
            "idJanusCible": idJanusSource,
            "typeSource": typeCible.name,
            "typeCible": typeSource.name,
            "name": "linkedTo"}
    post_response = session.post(url=relation_url, json=link, headers=header_with_token)
    if post_response.status_code == 201:
        print("SUCCESSFUL REQUEST :  " + str(post_response))
