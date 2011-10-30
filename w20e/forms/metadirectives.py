from zope.interface import Interface
from registry import Registry
from zope.schema import TextLine


class ISubmissionDirective(Interface):

    name = TextLine(
        title=u"Unique id of submission type",
        description=u"""""",
        required=True)

    factory = TextLine(
        title=u'Factory that creates the necessary object.',
        description=u'',
        required=True)


class IControlDirective(Interface):

    name = TextLine(
        title=u"Unique id of control type",
        description=u"""""",
        required=True)

    factory = TextLine(
        title=u'Factory that creates the necessary object.',
        description=u'',
        required=True)


def register_submission(_context, name, factory):

    _context.action(
        discriminator=('submission', name),
        callable=Registry.register_submission,
        args = (name, factory),
        )


def register_control(_context, name, factory):

    _context.action(
        discriminator=('control', name),
        callable=Registry.register_control,
        args = (name, factory),
        )
