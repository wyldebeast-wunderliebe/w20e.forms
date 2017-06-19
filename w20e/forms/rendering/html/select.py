from .templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implementer
from w20e.forms.registry import Registry
import collections


@implementer(IControlRenderer)
class SelectRenderer(object):

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        opts = []

        if renderable.vocab:

            vocab = Registry.get_vocab(renderable.vocab)

            if isinstance(vocab, collections.Callable):

                args = []
                if renderable.vocab_args:
                    args = renderable.vocab_args.split(",")

                opts = vocab(*args, **kwargs)

        opts.extend(renderable.options)

        value = form.data[renderable.bind]

        # some hacking for multiple type. sometimes the saved data is just a
        # plain old type (int) and we expect a list of strings in the template
        if fmtmap['multiple'] and fmtmap['multiple'].lower() == 'true':
            value = form.getFieldValue(renderable.id, lexical=False)
            if isinstance(value, collections.Sequence):  # just to be sure?
                value = [str(val) for val in value]

        if renderable.format == "full":

            res = get_template('select_full')(
                control=renderable,
                value=value,
                options=opts,
                fmtmap=fmtmap
                )

            print(res, file=out)

        else:

            res = get_template('select')(
                control=renderable,
                value=value,
                options=opts,
                multiple=fmtmap['multiple'],
                fmtmap=fmtmap
                )
            print(res, file=out)
