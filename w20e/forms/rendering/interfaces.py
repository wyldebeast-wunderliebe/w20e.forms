from zope.interface import Interface

class IRenderer(Interface):

    """ Renderers should... render. Anyway, this is just a marker """


class IControlRenderer(Interface):

    """ Renderer for single widget/control/(group).
    
    """

    def render(renderer, form, renderable, out, **kwargs):

        """ Render this control.First argument should be
        implementation of IRenderer. Out should be a printable output,
        like stdout or stringio.
        """
