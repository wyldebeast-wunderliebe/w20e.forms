from zope.interface import implements
from w20e.forms.interfaces import IControlGroup
from w20e.forms.formview import RenderableContainer
from renderables import Renderable


class Group(RenderableContainer, Renderable):

    implements(IControlGroup)

    def __init__(self, group_id, label="", **props):

        RenderableContainer.__init__(self)
        Renderable.__init__(self, group_id, **props)

        self.label = label


class FlowGroup(Group):

    """ Implement a grouping component that makes it's content flow,
    either horizontally or vertically. Possible orientations:
    h (horizontal), v (vertical).
    """

    def __init__(self, group_id, label="", orientation="v", **props):

        Group.__init__(self, group_id, label=label, **props)

        self.orientation = orientation


class GridGroup(Group):

    """ Implement a grouping component that lays out it's component
    in a strict grid.
    """

    def __init__(self, group_id, label="", cols=3, **props):

        Group.__init__(self, group_id, label=label, **props)

        self.cols = cols


class CardGroup(Group):

    """ Implement a grouping component that makes it's contents
    available as 'cards', where only one is visible at one given time.
    """

    def __init__(self, group_id, label="", **props):

        Group.__init__(self, group_id, label=label, **props)


class StepGroup(Group):

    """ Wizard like group as step in wizard process """

    def __init__(self, group_id, label="", **props):

        Group.__init__(self, group_id, label=label, **props)
