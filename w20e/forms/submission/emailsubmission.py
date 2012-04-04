import smtplib
import os

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

        SubmissionBase.__init__(self, **props)


    def submit(self, form, *args):

        data = form.data
        model = form.model

        if type(self.send_to)==str:
            self.send_to = [self.send_to]

        msg = MIMEMultipart()
        msg['From'] = self.send_from
        msg['To'] = COMMASPACE.join(self.send_to)
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

        msg.attach( MIMEText("\n".join(text)) )
        
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
        
