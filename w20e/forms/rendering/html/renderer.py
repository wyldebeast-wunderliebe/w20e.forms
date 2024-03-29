from zope.interface import implementer
from .templates import get_template
from w20e.forms.rendering.interfaces import IRenderer
from w20e.forms.rendering.baserenderer import BaseRenderer


FORM_HEADER = """<form class="w20e-form %s" method="post" action="%s"
  id="%s" enctype="multipart/form-data">"""


@implementer(IRenderer)
class HTMLRenderer(BaseRenderer):

    """ The HTML renderer expects to recive some kind of output
    stream, that can be used to append to. This can obviously be
    sys.stdout, but also a stringIO instance.
    """

    def __init__(self, **kwargs):

        BaseRenderer.__init__(self, **kwargs)

    def renderFrontMatter(self, form, out, errors=None, **kwargs):

        """ Render whatever needs to be rendered before the actual
        form components"""

        kwargs['action'] = getattr(form.submission, 'action',
                                   kwargs.get('action', ''))

        form_class = kwargs.get('form_class', '')
        form_class += " " + self.opts.get('class', '')
        kwargs['form_class'] = form_class.strip()
        kwargs['page_id'] = kwargs.get('page_id', '')
        kwargs['status_message'] = ''

        if kwargs['status'] in ["completed", "error"]:
            kwargs['status_message'] = getattr(form.submission,
                                               "status_" + kwargs.get('status',
                                                                      ''),
                                               kwargs.get('status', '')
                                               )
        template = get_template('frontmatter')
        template_html = template(form_id=form.id, **kwargs)
        out.write(template_html)
        # print(template_html, file=out)

        #if errors:
        #    print >> out, """<div class="alert alert-warning"></div>"""

    def renderBackMatter(self, form, out, errors=None, **opts):

        print("</form>", file=out)

    def render(self, form, renderable, out, errors=None, **kwargs):
        rtype = renderable.type
        renderer = self.getRendererForType(rtype, "html")
        renderer.render(self, form, renderable, out, errors=errors,
                        **kwargs)
