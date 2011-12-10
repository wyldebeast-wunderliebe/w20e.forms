from zope.interface import implements
from interfaces import IFormData
from data.field import Field
from ordereddict import OrderedDict


class FormData(object):

    implements(IFormData)

    def __init__(self, data=None):

        if not data:
            data = {}
        super(FormData, self).__init__()
        self._fields = OrderedDict()
        self.from_dict(data)

    def __repr__(self):

        reprlist = ["FormData:", ""]

        for field in self._fields.keys():

            value = self._fields[field].value

            # small hack for fields that have a dict as value (files)
            if isinstance(value, dict):
                if 'name' in value:
                    value = value['name']

            reprlist.append("%s: %s\n" % (field, value))

        return "\n".join(reprlist)

    def __getitem__(self, fieldId):

        """ Always return something... even if the data isn't
        there. This allows for a somewhat lax policy in evaluation of
        requiredness, relevance, etc.
        """

        try:
            return self._fields[fieldId].value
        except:
            return None

    def __setitem__(self, fieldId, val):

        """ Item assignment on formdata. Setting the value of a non existing
        field is NOT an error... """

        if not fieldId in self._fields:
            self._fields[fieldId] = Field(fieldId, val)
        else:
            self._fields[fieldId].value = val

    def getField(self, fieldId):

        return self._fields.get(fieldId, None)

    def addField(self, field):

        self._fields[field.id] = field

    def getFields(self):

        return self._fields.keys()

    def update(self, data, ignore_missing=True):

        """ Update self with fields from data arg """

        for field_id in data.getFields():
            field = data.getField(field_id)
            if self.getField(field_id):
                self.getField(field_id).value = field.value
            else:
                if not ignore_missing:
                    self.addField(Field(field.id, field.value))

    def as_dict(self):

        res = {}

        for field_id in self._fields.keys():

            res[field_id] = self._fields[field_id].value

        return res

    def from_dict(self, data=None):

        """ Set the form fields and values from a dict """
        if data:
            for key, val in data.items():
                self[key] = val
