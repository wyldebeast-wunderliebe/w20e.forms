from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
from .templates import get_template
from io import StringIO
import codecs
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class CardGroupRenderer(object):

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        def render_subs(sub):
            """ render the sub renderable """
            str_out = StringIO()
            out = codecs.getwriter('utf-8')(str_out)
            sub.extra_classes = (sub.extra_classes or "") + " card"
            renderer.render(form, sub, out, **kwargs)
            return out.getvalue().decode('utf-8')

        print(get_template('cardgroup')(
            group=renderable,
            fmtmap=fmtmap,
            render_subs = render_subs
            ), file=out)
