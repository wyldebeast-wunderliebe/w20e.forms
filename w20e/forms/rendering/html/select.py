from templates import get_template
from w20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements
from w20e.forms.registry import Registry


class SelectRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        opts = []
        
        if renderable.vocab:
            
            vocab = Registry.get_vocab(renderable.vocab)
            
            if callable(vocab):
                
                opts = vocab()
        else:
            opts = renderable.options

        value = form.data[renderable.bind]
        if renderable.format == "full":

            print >> out, get_template('select_full')(
                control=renderable, 
                value=value,
                options=opts,
                extra_classes=fmtmap['extra_classes']
                )

        else:

            print >> out, get_template('select')(
                control=renderable, 
                value=value,
                options=opts,
                multiple=fmtmap['multiple'],
                extra_classes=fmtmap['extra_classes']
                )
