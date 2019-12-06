from __future__ import absolute_import
from builtins import object
from zope.interface import implementer
from .interfaces import IFormData
from .data.field import Field
from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)


@implementer(IFormData)
class FormData(object):

    def __init__(self, data=None):

        if not data:
            data = {}
        super(FormData, self).__init__()
        self._fields = OrderedDict()
        self.from_dict(data)

    def __repr__(self):

        reprlist = ["FormData:", ""]

        for field in list(self._fields.keys()):

            value = self._fields[field].value

            # small hack for fields that have a dict as value (files)
            if isinstance(value, dict):
                if 'name' in value:
                    value = value['name']

            if isinstance(field, str):
                field = field.encode('utf-8')
            if isinstance(value, str):
                value = value.encode('utf-8')

            reprlist.append("%s: %s\n" % (field, value))

        return "\n".join(reprlist)

    def __json__(self, request):
        return self.as_dict()

    def __getitem__(self, fieldId):

        """ Always return something... even if the data isn't
        there. This allows for a somewhat lax policy in evaluation of
        requiredness, relevance, etc.
        """

        try:
            return self._fields[fieldId].value
        except:
            logger.exception('Could not retrieve value from field')
            return None

    def __setitem__(self, fieldId, val):

        """ Item assignment on formdata. Setting the value of a non existing
        field is NOT an error... """

        if fieldId not in self._fields:
            self._fields[fieldId] = Field(fieldId, val)
        else:
            self._fields[fieldId].value = val

    def getField(self, fieldId):

        return self._fields.get(fieldId, None)

    def addField(self, field):

        self._fields[field.id] = field

    def getFields(self):

        return list(self._fields.keys())

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

        for field_id in list(self._fields.keys()):
            res[field_id] = self._fields[field_id].value

        return res

    def from_dict(self, data=None, create_missing_fields=True):

        """ Set the form fields and values from a dict """
        self.clear()
        if data:
            for key, val in list(data.items()):
                if create_missing_fields:
                    self[key] = val
                else:
                    fld = self.getField(key)
                    if fld:
                        fld.value = val

    def clone(self):
        """ clone the data """
        return FormData(self.as_dict())

    def clear(self):
        """ clear all data """
        for fieldId in self.getFields():
            self._fields[fieldId].value = None
