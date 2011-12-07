from zope.interface import implements
from interfaces import IFormView
from rendering.html.renderer import HTMLRenderer
from StringIO import StringIO
import codecs


class RenderableContainer:

    def __init__(self):

        self._components = []
        self._componentmap = {}
        self._bindmap = {}

    def addRenderable(self, renderable):

        self._components.append(renderable)
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

    """ Visible part of the form, that holds controls and groups.
    """

    implements(IFormView)

    def __init__(self, renderer=HTMLRenderer, renderOpts=None):

        if not renderOpts:
            renderOpts = {}

        RenderableContainer.__init__(self)
        self.renderer = renderer(**renderOpts)

    def renderFrontMatter(self, form):

        """ Render form front matter """

        str_out = StringIO()
        out = codecs.getwriter('utf-8')(str_out)

        self.renderer.renderFrontMatter(form, out)

        return out.getvalue()

    def renderBackMatter(self, form):

        """ Render form back matter... """

        str_out = StringIO()
        out = codecs.getwriter('utf-8')(str_out)

        self.renderer.renderBackMatter(form, out)

        return out.getvalue()

    def renderForm(self, form):

        """ Render form content only """

        str_out = StringIO()
        out = codecs.getwriter('utf-8')(str_out)

        for item in self.getRenderables():

            self.renderer.render(form, item, out)

        return out.getvalue()

    def render(self, form, errors=None):

        """ Render all (front, content and back) """

        str_out = StringIO()
        out = codecs.getwriter('utf-8')(str_out)

        self.renderer.renderFrontMatter(form, out)

        for item in self.getRenderables():

            self.renderer.render(form, item, out, errors=errors)

        self.renderer.renderBackMatter(form, out)

        return out.getvalue()
