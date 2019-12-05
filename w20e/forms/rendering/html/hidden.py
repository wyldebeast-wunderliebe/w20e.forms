from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements
from .templates import get_template


class HiddenRenderer(object):

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Hidden to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        try:
            value = form.getFieldValue(renderable.bind)
        except:
            value = ""

        print(get_template('hidden')(
            control=renderable,
            value=value,
            fmtmap=fmtmap), file=out)
