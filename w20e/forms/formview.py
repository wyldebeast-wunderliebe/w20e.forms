from zope.interface import implements
from interfaces import IFormView
from rendering.html.renderer import HTMLRenderer
from StringIO import StringIO
import codecs
from config import PAGE_ID
from w20e.forms.form import FormValidationError
from w20e.forms.exceptions import ProcessingException


class RenderableContainer:

    is_group = True

    def __init__(self):

        self._components = []
        self._componentmap = {}
        self._bindmap = {}

    def rmRenderable(self, renderable_id):

        renderable = self._componentmap.pop(renderable_id)
        self._components.remove(renderable)

    def addRenderable(self, renderable, pos=None):

        """ Add renderable. If pos is given, insert into that
        position, otherwise just append"""

        if pos is None:
            self._components.append(renderable)
        else:
            self._components.insert(pos, renderable)
        self._componentmap[renderable.id] = renderable

        if hasattr(renderable, 'bind'):
            self._bindmap[renderable.bind] = renderable

        try:
            for r in renderable.getRenderables():
                self._recurseAddRenderable(r)
        except:
            pass

    def _recurseAddRenderable(self, renderable):

        self._componentmap[renderable.id] = renderable
        if hasattr(renderable, 'bind'):
            self._bindmap[renderable.bind] = renderable

        try:
            for r in renderable.getRenderables():
                self._recurseAddRenderable(r)
        except:
            pass

    def getRenderables(self, recursive=False):

        if recursive:
            return self._componentmap.values()
        else:
            return self._components

    def getRenderable(self, id):

        return self._componentmap.get(id, None)

    def getRenderableByBind(self, bind):

        return self._bindmap.get(bind, None)


class FormView(RenderableContainer):

    """ Visible part of the form, that holds controls and groups and
    handles rendering logic.
    """

    implements(IFormView)

    def __init__(self, renderer=HTMLRenderer, **opts):

        RenderableContainer.__init__(self)
        self.renderer = renderer(**opts)

    def get_renderables(self, form, current_page_id, direction="next"):

        """ Find the set of renderables to show. Return none, if
        there's nothing let to render. Direction can be 'previous' or 'next'.
        """

        pages = self.getRenderables()

        if not self.renderer.opts.get("multipage", False):
            return pages

        page_ids = [p.id for p in pages]

        try:
            moreorless = direction=="previous" and -1 or 1
            page_index = page_ids.index(current_page_id) + moreorless
        except:
            page_index = 0

        if page_index >= len(page_ids):
            page_index = 0

        page = None

        while page_index < len(pages):

            page = pages[page_index]

            if page.is_group and form.model.isGroupRelevant(page, form.data):
                break
            elif not page.is_group and form.model.isRelevant(page, form.data):
                break
            else:
                page_index += 1

        renderables = None
        if page:
            renderables = [page]

        return renderables

    def is_last_page(self, page_id):

        if not self.renderer.opts.get("multipage", False):
            return True
        else:
            return self.getRenderables()[-1].id == page_id

    def get_current_page(self, page_id):

        if not self.renderer.opts.get("multipage", False):
            return self

        return self.getRenderable(page_id)

    def render(self, form, errors=None, status='', data=None,
               context=None, **opts):

        """ Render all (front, content and back). Calling code should
        take care of the case where there is nothing to render..."""

        str_out = StringIO()
        out = codecs.getwriter('utf-8')(str_out)

        direction = "next"

        if data is None:
            data = {}

        if data.get("w20e.forms.previous", None):
            direction = "previous"

        page_id = data.get(PAGE_ID, None)

        if errors:
            page = self.get_current_page(page_id)
            if page:
                if hasattr(page, 'id'):
                    page_id = page.id
                else:
                    page_id = None
                renderables = page.getRenderables()
            else:
                renderables = []
        else:
            renderables = self.get_renderables(
                form,
                page_id,
                direction=direction
                )
            if renderables:
                page_id = renderables[0].id

        if not renderables:
            raise Exception("Nothing to render!")

        self.renderer.renderFrontMatter(form, out, errors,
                                        page_id=page_id,
                                        status=status, **opts)

        for item in renderables:

            self.renderer.render(form, item, out, errors=errors,
                    data=data, context=context)

        self.renderer.renderBackMatter(form, out, errors, **opts)

        return out.getvalue()

    def process_data(self, form, view, data=None):

        """ Process data for the form. Usually this will involve data
        from a request.
        """

        if not data:
            data = {}

        if view.is_group:
            renderables = view.getRenderables()
        else:
            renderables = [view]

        for renderable in renderables:

            if callable(renderable.processInput):

                fld = form.data.getField(renderable.bind)

                if fld:  # could be a flowgroup e.g.

                    if not form.model.isRelevant(fld.id, form.data):
                        continue

                    datatype = form.model.get_field_datatype(fld.id)

                    try:
                        fld.value = renderable.processInput(data,
                                datatype=datatype)
                    except ProcessingException:
                        pass


            if renderable.getRenderables:
                self.process_data(form, renderable, data)

    def handle_form(self, form, data):

        """ Handle the form. Override this method if you
        wish... 'data' is something dict-ish, usually a request...
        Handle form will take care of setting data and validating the
        form, or in the case of multipage forms, the current page. The
        method will return the status, and map of errors, where keys
        are field id's. Status can be one of:

          completed - Form is completed and valid
          valid - Form is valid, but (only for multipage forms) not completed
          error - Form is invalid. In this case the errors map will also be
                  filled with the errors found.

        """

        status = "init"
        errors = {}

        if data.get("w20e.forms.process", False):

            fields = None

            if self.renderer.opts.get("multipage", False):

                fields = []
                page = self.get_current_page(data.get("w20e.forms.page"))

                # Page could actually be a single control
                #
                if page.is_group:
                    for renderable in page.getRenderables(recursive=True):

                        fld = form.data.getField(renderable.bind)

                        if fld:
                            fields.append(fld.id)
                else:
                    fields = [page.id]

            self.process_data(
                form,
                self.get_current_page(data.get("w20e.forms.page")),
                data)

            status = 'processed'

            try:
                if self.is_last_page(data.get("w20e.forms.page")):
                    form.validate()
                    status = 'completed'
                else:
                    form.validate(fields=fields)
                    status = 'valid'

            except FormValidationError, fve:
                errors = fve.errors
                status = 'error'

        return (status, errors)
