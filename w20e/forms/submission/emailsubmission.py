import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

from submission import SubmissionBase


class EmailSubmission(SubmissionBase):

    type = "email"

    """ Submission handler that submits data to content type.
    """

    def __init__(self, **props):

        """ Email submission does... well, you get the idea... """
        
        self.subject = self.reply_to = self.send_from = self.send_to = ""

        SubmissionBase.__init__(self, **props)

    def submit(self, form, *args):

        data = form.data
        model = form.model

        if type(self.send_to) == str:
            self.send_to = [self.send_to]

        msg = MIMEMultipart()

        # Special treatment for from... Check if it refers to a form field
        #
        if re.match("\$\{.+\}", self.send_from):
            try:
                var = re.match("\$\{(.+)\}", self.send_from).groups()[0]
                self.send_from = form.getFieldValue(var)
            except:
                pass

        # Special treatment for reply_to... Check if it refers to a form field
        #
        if re.match("\$\{.+\}", self.reply_to):
            try:
                var = re.match("\$\{(.+)\}", self.reply_to).groups()[0]
                self.reply_to = form.getFieldValue(var)
            except:
                pass

        msg['From'] = self.send_from
        msg['To'] = COMMASPACE.join(self.send_to)
        if hasattr(self, 'reply_to') and self.reply_to:
            msg['Reply-To'] = self.reply_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        text = [getattr(self, 'pre_text', "")]
        files = []

        for field in data.getFields():

            if not self.isFile(field, model):

                text.append("%s: %s" % (field,
                                        form.getFieldValue(field,
                                                           default=data[field],
                                                           lexical=True)))

            else:

                files.append(data[field])

        text.append(getattr(self, 'post_text', ""))

        msg.attach(MIMEText("\n".join(text)))

        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(f)
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % "pipo.txt")
            msg.attach(part)

        smtp = smtplib.SMTP(getattr(self, 'host', "localhost"),
                            getattr(self, 'port', "25"))

        if hasattr(self, 'tls'):
            smtp.starttls()

        if hasattr(self, 'user'):
            smtp.login(self.user, getattr(self, 'pwd', ''))

        smtp.sendmail(self.send_from, self.send_to, msg.as_string())
        smtp.close()

    def retrieve(self, *args):

        return None

    def isFile(self, field, model):

        """ Is it a file? You may wish to override this call for your specific
        deployment to determine file values. """

        if field in getattr(self, 'files', "").split(","):
            return True
        else:
            return False
