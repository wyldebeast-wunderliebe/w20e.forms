from builtins import object
import zlib
from ZODB.blob import Blob as Blob
from copy import deepcopy


class TheBlob(object):
    """
    contain a Blob which we can also use for compressed data
    Note: you can't subclass a Blob (google for it) so we use composition
    instead of subtyping
    """

    def __init__(self, data=None, compress=False):
        """ instantiate the blob file """

        self._blob = Blob()
        self._compress = compress

        if data:
            self.set(data)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        new_blob = Blob()
        memo[id(new_blob)] = new_blob

        memo[id(new_blob)] = new_blob
        setattr(result, '_compress', self._compress)
        setattr(result, '_blob', new_blob)
        result.set(self.get())
        return result

    def set(self, data):
        """ store the data in the blob. Compress if necessary """

        if self._compress:
            self._blob.open('w').write(zlib.compress(data))
        else:
            self._blob.open('w').write(data)

    def get(self):
        """ retrieve the blob data. Decompress if necessary """

        if self._compress:
            return zlib.decompress(self._blob.open('r').read())
        else:
            return self._blob.open('r').read()

    def open_blob(self, mode="r"):
        """
        pass on to the blob. Not sure if this is a good idea with
        regards to persistance..
        """
        return self._blob.open(mode)
