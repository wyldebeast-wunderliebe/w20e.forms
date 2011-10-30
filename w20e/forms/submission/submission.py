from w20e.forms.submission.interfaces import ISubmission
from zope.interface import implements


class SubmissionBase:

    implements(ISubmission)


    def __init__(self, **props):

        """ Initialize base submission. """

        self._custom_props = props.keys()
        self.__dict__.update(props)

        self.type = self.__class__.__name__.lower()


    def submit(self, *args):

        """ Do nothing much... """


    def retrieve(self):

        """ Same, same... """

