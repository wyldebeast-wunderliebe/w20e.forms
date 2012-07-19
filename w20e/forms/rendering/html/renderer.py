from zope.interface import implements

from w20e.forms.rendering.interfaces import IRenderer
from w20e.forms.rendering.baserenderer import BaseRenderer


FORM_HEADER = """<form class="w20e-form %s" method="post" action="%s"
  id="%s" enctype="multipart/form-data">"""


class HTMLRenderer(BaseRenderer):

    """ The HTML renderer expects to recive some kind of output
    stream, that can be used to append to. This can obviously be
    sys.stdout, but also a stringIO instance.
    """

    implements(IRenderer)

    def __init__(self, **kwargs):

        BaseRenderer.__init__(self, **kwargs)

    def renderFrontMatter(self, form, out, errors=None, **kwargs):
        """ Render whatever needs to be rendered before the actual form
        components """

        print >> out, FORM_HEADER % \
              (kwargs.get("form_class", ""),
               getattr(form.submission, 'action', kwargs.get('action', '')),
               form.id)
        print >> out, """<input type="hidden" name="formprocess" value="1"/>"""

        if 'currentpage' in kwargs:
            currentpage = kwargs['currentpage']
            output = """<input type="hidden" name=""" \
                    """'w20e.forms.currentpage' value="%s"/>""" % currentpage
            print >> out, output

        #if errors:
        #    print >> out, """<div class="alert alert-warning"></div>"""

    def renderBackMatter(self, form, out, errors=None, request=None, **opts):

        print >> out, "</form>"

    def render(self, form, renderable, out, errors=None, **kwargs):

        #try:
        rtype = renderable.type
        renderer = self.getRendererForType(rtype, "html")()
        renderer.render(self, form, renderable, out, errors=errors,
                        **kwargs)
        #except:

        #    print >> out, "<!-- No renderer found for %s! -->" % rtype
