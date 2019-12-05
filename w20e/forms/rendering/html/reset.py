from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class ResetRenderer(object):

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        print(get_template('reset')(
            control=renderable,
            fmtmap=fmtmap
            ), file=out)
