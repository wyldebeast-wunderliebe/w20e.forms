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
        data_attr = self.bind or self.id

        present = data_attr in data

        if not present or data[data_attr] == None or data[data_attr] == '':
            raise ProcessingException("no file. skip it")

        if data[data_attr] == '1':
            fieldstorage = data.get("%s-new" % data_attr, None)
            # comparing the fieldstorage with the unary 'not'
            # operator doesn't work.. so weird looking check:
            if fieldstorage == '' or fieldstorage == None:
                raise ProcessingException("empty file. Skip this!")

        if data.get("%s-new" % data_attr, None) is not None:
            _file = data["%s-new" % data_attr]
        else:
            _file = data[data_attr]


        return {'data': _file.value, 'name': _file.filename}


    def lexVal(self, value):

        if type(value) == type({}):
            return value.get("name", "")
        else:
            return value
