from submission import SubmissionBase


class NoSubmission(SubmissionBase):

    """ Submission implementation that does... nothing! """

    def __init__(self, **props):

        SubmissionBase.__init__(self, **props)
        self.type = "none"
