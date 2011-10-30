import os
from ..utils import find_file


class FormFile:

    def __init__(self, filename):

        self.filename = filename

        if not os.path.isfile(self.filename):
            raise ValueError("No such file", self.filename)


    def modified(self):

        """ Return last modified timestamp """

        return os.path.getmtime(self.filename)
