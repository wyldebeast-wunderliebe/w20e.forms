from w20e.forms.rendering.control import File
from w20e.forms.exceptions import ProcessingException


class PyramidFile(File):

    """ File upload control """

    def __init__(self, *args, **kwargs):

        File.__init__(self, *args, **kwargs)
        self.type = "file"


    def processInput(self, data=None, datatype="file"):

        """ File data is stored in value field """

        if not data:
            data = {}

        assert datatype == 'file', 'expected a file as datatype'

        _file = None

        present = self.id in data

        if not present or data[self.id] == None or data[self.id] == '':
            raise ProcessingException("no file. skip it")

        if data[self.id] == '1':
            fieldstorage = data.get("%s-new" % self.id, None)
            # comparing the fieldstorage with the unary 'not'
            # operator doesn't work.. so weird looking check:
            if fieldstorage == '' or fieldstorage == None:
                raise ProcessingException("empty file. Skip this!")

        if data.get("%s-new" % self.id, None) is not None:
            _file = data["%s-new" % self.id]
        else:
            _file = data[self.id]


        return {'data': _file.value, 'name': _file.filename}


    def lexVal(self, value):

        if type(value) == type({}):
            return value.get("name", "")
        else:
            return value
