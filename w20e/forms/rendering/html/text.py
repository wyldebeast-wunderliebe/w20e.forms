from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer


@implementer(IControlRenderer)
class TextRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        if renderable.bind:
            # only change text if a value was calculated
            calculate_found = False
            for props in form.model.getFieldProperties(renderable.bind):
                if props.getCalculate():
                    calculate_found = True
                    break

            if calculate_found:
                try:
                    value = form.getFieldValue(renderable.bind, lexical=True)
                    # TODO: not sure about this string conversion..
                    # leave unicode values intact.
                    # if not isinstance(value, str):
                    #     value = str(value)
                    # if isinstance(value, str):
                    #     value = value.decode('utf-8')
                    fmtmap['text'] = value
                except:
                    pass

        rendered = get_template("text")(
            control=renderable,
            text=fmtmap['text'],
            fmtmap=fmtmap)

        print(rendered, file=out)
