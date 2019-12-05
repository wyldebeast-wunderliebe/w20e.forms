from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
from .templates import get_template
from io import StringIO
import codecs
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class StepGroupRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        currentpage = kwargs.get('currentpage', None)

        str_out = StringIO()
        sub_out = codecs.getwriter('utf-8')(str_out)

        for sub_renderable in renderable.getRenderables():
            stepgroup_classes = "step"

            item = sub_renderable

            if currentpage and item.id == currentpage:
                stepgroup_classes += " active"

            renderer.render(form, item, sub_out,
                    stepgroup_classes=stepgroup_classes, **kwargs)

        steps = [{'id': step.id, "class": "", 'label': step.label} for step in \
                 renderable.getRenderables()]

        steps[0]['class'] = "first"
        steps[-1]['class'] = "last"

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        print(get_template('stepgroup')(
            group=renderable,
            steps=steps,
            content=str_out.getvalue().decode("utf-8"),
            fmtmap=fmtmap
            ), file=out)
