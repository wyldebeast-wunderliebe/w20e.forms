from BTrees.OOBTree import OOBTree
from ZODB.blob import Blob
from submission import SubmissionBase
from w20e.forms.formdata import FormData
from w20e.forms.data.field import Field


DATA_ATTR_NAME = "_w20e_forms_data"


class AttrStorage(SubmissionBase):

    """ Submission handler that submits data to content type. The data
    will be set as dict onto the given attribute name.
    """

    type = "attr"

    def __init__(self, **props):

        """ AttrStorage uses simple attribute storage to store the
        whole data container on the context.
        """

        SubmissionBase.__init__(self, **props)

        self.attr_name = props.get("attr_name", DATA_ATTR_NAME)
        self.use_blobstorage = props.get("use_blobstorage", False)

    def _get_storage(self, context):
        storage = getattr(context, self.attr_name, None)
        if storage is None:
            setattr(context, self.attr_name, OOBTree())
        return getattr(context, self.attr_name)

    def _store_blob(self, storage, field):
        """ store in blob storage """

        # handle null data, don't use blob storage..
        if not field.value or not field.value['data']:
            storage[field.id] = None
        else:
            # only if we get raw filedata store it in a blob..
            #if it's already a blob,it hasn't changed, so no need to store
            if isinstance(field.value['data'], str):
                # we have data, store as Blob
                container = storage.get(field.id) or {'name': None, 'data': Blob()}
                container['name'] = field.value['name']
                f = container['data'].open('w')
                f.write(field.value['data'])
                f.close()
                storage[field.id] = container

    def _retrieve_blob(self, context, storage, field_id):
        data = storage.get(field_id)

        # check for non-blob storage file, and migrate on-the-fly if necessary
        if data and isinstance(data['data'], str):
            self._migrate_blob(storage, field_id)
            context._p_changed = 1  # trigger update
            data = storage.get(field_id)

        if data:
            container = {}
            container['name'] = data['name']
            container['data'] = data['data']
            return container

    def _use_blobstorage(self, form, field_id):
        store_blob = False
        if self.use_blobstorage:
            for props in form.model.getFieldProperties(field_id):
                datatype = props.getDatatype()
                if datatype and datatype == 'file':
                    store_blob = True
                    break
        return store_blob

    def submit(self, form, context, *args):

        """ Submit data. This involves storing it onto the content
        type. The submit call should provide the context as first
        param.
        """

        storage = self._get_storage(context)

        # store fields, and check for blobs
        for field_id in form.data.getFields():
            field = form.data.getField(field_id)
            store_blob = self._use_blobstorage(form, field_id)

            if store_blob:
                self._store_blob(storage, field)
            else:
                storage[field.id] = field.value

            context._p_changed = 1

    def _migrate_blob(self, storage, field_id):
        """ migrate simple attrstorage files to blobstorage """
        field = Field(field_id, storage.get(field_id))
        container = {'name': None, 'data': Blob()}
        container['name'] = field.value['name']
        f = container['data'].open('w')
        f.write(field.value['data'])
        f.close()
        storage[field.id] = container

    def retrieve(self, form, context, *args):
        """ Restore data. """

        storage = self._get_storage(context)

        data = FormData()

        for field_id in form.data.getFields():
            store_blob = self._use_blobstorage(form, field_id)
            if store_blob:
                data.addField(Field(field_id, self._retrieve_blob(context, storage,
                    field_id)))
            else:
                data.addField(Field(field_id, storage.get(field_id)))

        return data
