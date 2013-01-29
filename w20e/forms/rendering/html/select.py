from templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements
from w20e.forms.registry import Registry


class SelectRenderer(object):

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        opts = []

        if renderable.vocab:

            vocab = Registry.get_vocab(renderable.vocab)

            if callable(vocab):

                args = []
                if renderable.vocab_args:
                    args = renderable.vocab_args.split(",")

                opts = vocab(*args, **kwargs)
        else:
            opts = renderable.options

        value = form.data[renderable.bind]
        if renderable.format == "full":

            print >> out, get_template('select_full')(
                control=renderable,
                value=value,
                options=opts,
                fmtmap=fmtmap
                )

        else:

            print >> out, get_template('select')(
                control=renderable,
                value=value,
                options=opts,
                multiple=fmtmap['multiple'],
                fmtmap=fmtmap
                )
