import smtplib
from pydal.validators import IS_EMAIL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class PhanterPWAMailSender(object):
    """docstring for PhanterPWAMailSender"""

    def __init__(
            self,
            sender_email,
            password_sender,
            receiver_email,
            subject="Test",
            text_mensage="Test",
            html_mensage="<html><b>Test</b></html>",
            alternative_sender=None,
            server='127.0.0.1',
            port=25,
            use_tls=False,
            use_ssl=False):
        super(PhanterPWAMailSender, self).__init__()
        self.sender_email = sender_email
        self.password_sender = password_sender
        self.receiver_email = receiver_email
        self.subject = subject
        self.text_mensage = text_mensage
        self.html_mensage = html_mensage
        self.alternative_sender = alternative_sender
        self.server = server
        self.port = port
        self.use_tls = use_tls
        self.use_ssl = use_ssl

    @property
    def sender_email(self):
        return self._sender_email

    @sender_email.setter
    def sender_email(self, value):

        if IS_EMAIL()(value)[1] is None:
            self._sender_email = value
        else:
            raise ValueError("The sender mail is not valid mail. Given: {0}".format(value))

    @property
    def receiver_email(self):
        return self._receiver_email

    @receiver_email.setter
    def receiver_email(self, value):
        if IS_EMAIL()(value)[1] is None:
            self._receiver_email = value
        else:
            raise ValueError("The receiver mail is not valid mail. Given: {0}".format(value))

    @property
    def alternative_sender(self):
        return self._alternative_sender

    @alternative_sender.setter
    def alternative_sender(self, value):
        if value is not None:
            if IS_EMAIL()(value)[1] is None:
                self._alternative_sender = value
            else:
                raise ValueError("The alternative mail is not valid mail. Given: {0}".format(value))
        else:
            self._alternative_sender = None

    def send(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.alternative_sender or self.sender_email
        message["To"] = self.receiver_email
        text = MIMEText(self.text_mensage, "plain")
        html = MIMEText(self.html_mensage, "html")
        message.attach(text)
        message.attach(html)
        if self.use_ssl:
            host = smtplib.SMTP_SSL(self.server, self.port)
        else:
            host = smtplib.SMTP(self.server, self.port)
        if self.use_tls:
            host.starttls()

        host.login(self.sender_email, self.password_sender)
        host.sendmail(
            self.sender_email, self.receiver_email, message.as_string()
        )
