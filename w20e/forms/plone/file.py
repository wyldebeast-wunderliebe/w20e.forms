from w20e.forms.rendering.control import File


class PloneFile(File):

    """ File upload control """

    def __init__(self, *args, **kwargs):

        File.__init__(self, *args, **kwargs)
        self.type = "file"

    def processInput(self, data=None):

        """ File data is stored in value field """

        if not data:
            data = {}

        _file = None

        new_input = data.get("%s-new" % self.id, None)
        new_data = None
        if new_input:
            new_data = new_input.read()
            new_input.seek(0)  # reset the pointer

        if data[self.id] == '1' and not new_data:
            raise "Skip this!"

        if new_data:
            _file = data["%s-new" % self.id]
        else:
            _file = data[self.id]

        # if we don't have file data, return None
        value = None

        file_data = _file.read()
        if file_data:
            value = {'data': file_data, 'name': _file.filename}

        return value

    def lexVal(self, value):

        if type(value) == type({}):
            return value.get("name", "")
        else:
            return value
