from zope.interface import implements
from templates import get_template
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

        """ Render whatever needs to be rendered before the actual
        form components"""

        kwargs['action'] = getattr(form.submission, 'action',
                                   kwargs.get('action', ''))
        kwargs['form_class'] = kwargs.get('form_class', '')
        kwargs['page_id'] = kwargs.get('page_id', '')
        kwargs['status_message'] = ''

        if kwargs['status'] in ["completed", "error"]:
            kwargs['status_message'] = getattr(form.submission,
                                               "status_" + kwargs.get('status',
                                                                      ''),
                                               kwargs.get('status', '')
                                               )

        print >> out, get_template('frontmatter')(
            form_id=form.id,
            **kwargs
            )

        #if errors:
        #    print >> out, """<div class="alert alert-warning"></div>"""

    def renderBackMatter(self, form, out, errors=None, **opts):

        print >> out, "</form>"

    def render(self, form, renderable, out, errors=None, **kwargs):

        rtype = renderable.type
        renderer = self.getRendererForType(rtype, "html")
        renderer.render(self, form, renderable, out, errors=errors,
                        **kwargs)
