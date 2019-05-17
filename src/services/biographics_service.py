import base64
import json
from src.variables import biographics_url

def create_dto_biographic(biographics, session, header_with_token):
    # with open(biographics.biographicsImage, "rb") as image:
    #     f = image.read()
    #     b = bytearray(f)
    #     decode = base64.b64encode(b).decode('UTF-8')

    bio = {
        "biographicsFirstname": biographics.biographicsFirstname,
        "biographicsName": biographics.biographicsName,
        "biographicsImageContentType": biographics.biographicsImageContentType,
        "biographicsImage": biographics.biographicsImage
    }

    post_response = session.post(url = biographics_url, json = bio, headers = header_with_token)
    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF BIOGRAPHICS IS :" + str(target_ID))
        return target_ID