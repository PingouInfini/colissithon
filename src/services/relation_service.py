from src.variables import relation_url


def bind_object_to_biographics(biographics_id, target_ID, session, header_with_token):
    link = {"idJanusSource": biographics_id,
            "idJanusCible": target_ID,
            "typeSource": "Biographics",
            "typeCible": "RawData"}
    post_response = session.post(url=relation_url, json=link, headers=header_with_token)
    print(str(post_response) + "   : lien bio-rawdatas bien créé")