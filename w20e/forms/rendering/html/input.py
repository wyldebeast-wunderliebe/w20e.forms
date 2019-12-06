from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import object
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer
from .templates import get_template


@implementer(IControlRenderer)
class InputRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        # the input renderer is also used for date + datetime classes
        # in that case we can use the html capable browser to set the
        # input type to 'date' or 'datetime'
        fmtmap['input_type'] = 'text'
        if fmtmap['type'] in ('date', 'datetime', 'month'):
            fmtmap['input_type'] = fmtmap['type']

        try:
            value = form.getFieldValue(renderable.bind, lexical=True)
            # TODO: not sure about this string conversion..
            # leave unicode values intact.
            if not isinstance(value, str):
                value = str(value)
            if isinstance(value, str):
                value = value.decode('utf-8')
        except:
            value = u''

        if renderable.rows > 1:

            tpl = get_template("textarea")
        else:
            tpl = get_template("input")

        html = tpl(
            control=renderable,
            value=value,
            fmtmap=fmtmap
        )
        out.write(html)
        # print(, file=out)
