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

    def getNextPage(self, request, form, errors):
        """ find the next active page """

        if not request:
            return None

        forward = request.get('submit.next', None)
        backward = request.get('submit.previous', None)
        currentpage = request.get('w20e.forms.currentpage', None)
        groups = [s for s in self.getRenderables() if s.type == 'stepgroup']
        for stepgroup in groups:
            # TODO: can we have other groups than flowgroups here?
            steps = [s for s in stepgroup.getRenderables() if \
                    s.type == 'flowgroup']

            firstpage = steps and steps[0].id or ''

            if not currentpage and steps:
                # TODO should we check for the first relevant page instead?
                return firstpage

            # what direction are we going?
            if forward:
                pass  # default action
            elif backward:
                # clone the steps, and reverse them
                steps = steps[:]  # clone so we don't change the original order
                steps.reverse()
            else:
                return currentpage

            # find current  + next step
            found = False
            for s in steps:
                if found:
                    # check if this step is relevant
                    if form.model.isGroupRelevant(s, form.data):
                        # show the next or previous requested step
                        # first clear the erros from this step (no alerts)
                        if errors:
                            children = [
                                    child.id for child in s.getRenderables()]
                            error_list = errors.keys()
                            error = set(children).intersection(set(error_list))
                            for e in error:
                                del errors[e]
                        return s.id
                    continue
                if s.id == currentpage:
                    found = True
                    # only allow to go forward if current page has no errors
                    if forward:
                        children = [child.id for child in s.getRenderables()]
                        error_list = errors and errors.keys() or []
                        error = set(children).intersection(set(error_list))
                        if error:
                            return currentpage

            return currentpage

    def render(self, form, errors=None, status=None, request=None,
               context=None, **opts):

        """ Render all (front, content and back) """

        str_out = StringIO()
        out = codecs.getwriter('utf-8')(str_out)

        # find current page in case we have a multi-page form
        currentpage = self.getNextPage(request, form, errors)

        self.renderer.renderFrontMatter(form, out, errors,
                                        currentpage=currentpage, **opts)

        for item in self.getRenderables():

            self.renderer.render(form, item, out, errors=errors,
                    request=request, currentpage=currentpage, context=context)

        self.renderer.renderBackMatter(form, out, errors, request, **opts)

        return out.getvalue()
