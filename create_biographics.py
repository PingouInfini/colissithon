# @TODO Export des méthodes dans une autre classe -> résoudre TypeError: create_biographics() takes no arguments

class create_biographics:
    
    def __init__(self):
        print("init create_biographics")
        pass

    def create_biographics2(self, biographics, session, header_with_token, biographics_url):
        print("create_biographics // create_biographics")
        with open(biographics.biographicsImage, "rb") as image:
            f = image.read()
            b = bytearray(f)
            decode = base64.b64encode(b).decode('UTF-8')

        # request to insight
        #bio = "{\"biographicsFirstname\": \"" + str(biographics.biographicsFirstname) + "\", \"biographicsName\": \"" + str(biographics.biographicsName) + "\"}"
        bio = {
            "biographicsFirstname": biographics.biographicsFirstname,
            "biographicsName": biographics.biographicsName,
            "biographicsImageContentType" : biographics.biographicsImageContentType,
            "biographicsImage" : str(decode)
        }

        print ("##############################################"  + str(bio))
        postResponse = session.post(url=biographics_url, json=bio, headers=header_with_token)
        if postResponse.status_code == 201 :
            print(str(postResponse) + "     INCHALLAH")
            print (str(postResponse.content))
            data  = json.loads(postResponse.content)
            bio_id = data["id"]
            return bio_id
        else :
            print ("ERREUR : " +str(postResponse) )