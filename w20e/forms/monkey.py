from ZODB.blob import Blob as Blob

def get(self):

    return self.open('r').read()

setattr(Blob, "get", get)

