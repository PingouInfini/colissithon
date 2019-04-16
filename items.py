
class biographics :

    def __init__(self, biographicsFirstname, biographicsName, biographicsImage, biographicsImageContentType):
        self.biographicsName = biographicsName
        self.biographicsFirstname = biographicsFirstname
        self.biographicsImage = biographicsImage
        self.biographicsImageContentType = biographicsImageContentType

class raw_data :

    def __init__(self, rawDataName, rawDataData, rawDataDataContentType, rawDataCoordinates, rawDataContent, rawDataSourceType, rawDataSourceUri, rawDataCreationDate):

        #INDISPENSABLE
        self.rawDataName = rawDataName

        # Pour les images
        self.rawDataData = rawDataData
        self.rawDataDataContentType = rawDataDataContentType

        self.rawDataCoordinates = rawDataCoordinates

        self.rawDataContent = rawDataContent

        self.rawDataSourceType = rawDataSourceType

        self.rawDataSourceUri = rawDataSourceUri

        self.rawDataCreationDate = rawDataCreationDate

class relation_bio_data :

    def __init__(self, idJanusSource, idJanusCible, name, typeSource, typeCible):

        self.idJanusSource = idJanusSource
        self.idJanusCible = idJanusCible
        self.name = name
        self.typeSource = typeSource
        self.typeCible = typeCible

