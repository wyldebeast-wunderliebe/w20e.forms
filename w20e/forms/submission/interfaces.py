from zope.interface import Interface, Attribute


class ISubmission(Interface):

    """ Handle submission of data """

    type = Attribute(""" type of submission """)

    def submit(form, *args):

        """ Submit data to destination
        """

    def retrieve(form, *args):

        """ If the handler supports it, retrieve the data. Obviously,
        this may prove rather awkward when using email submission...
        The data retrieved should be an instance of FormData.
        """
