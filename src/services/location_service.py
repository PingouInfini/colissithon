import json
from src.variables import location_url


def create_dto_location(location, session, header_with_token):

    if location.locationType is not None:
        location_json = {
            "locationName": location.locationName,
            "locationType": location.locationType,
            "locationCoordinates": location.locationCoordinates,
        }
    else:
        location_json = {
            "locationName": location.locationName,
            "locationCoordinates": location.locationCoordinates,
        }

    post_response = session.post(url=location_url, json=location_json, headers=header_with_token)
    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF BIOGRAPHICS IS :" + str(target_ID))
        return target_ID