"""
Title: XmlConstructor

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

Send emails
"""

import smtplib
from pydal.validators import IS_EMAIL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailSender(object):
    """
    :param email_sender: Email used in sending
    :param password_sender: Email password used when sending
    :param email_receiver: Recipient email
    :param subject: Email title
    :param text_message: Plain text message
    :param html_message: Html format message
    :param alternative_sender: Reply email
    :param server: Server address
    :param port: Used port
    :param use_tls: Used tls
    :param use_ssl: Used ssl
    """

    def __init__(
            self,
            email_sender: str,
            password_sender: str,
            email_receiver: str,
            subject: str="Test",
            text_message: str="Test",
            html_message: str="<html><b>Test</b></html>",
            alternative_sender: (str, None)=None,
            server: str='127.0.0.1',
            port: int=25,
            use_tls: bool=False,
            use_ssl: bool=False):
        super(MailSender, self).__init__()
        self.email_sender = email_sender
        self.password_sender = password_sender
        self.email_receiver = email_receiver
        self.subject = subject
        self.text_message = text_message
        self.html_message = html_message
        self.alternative_sender = alternative_sender
        self.server = server
        self.port = port
        self.use_tls = use_tls
        self.use_ssl = use_ssl

    @property
    def email_sender(self) -> str:
        """Get ot Set the email sender.

        :GET:

            Get the email sender

        :SET:
            When adding an email, it is validated, if it is not a valid email it returns a ValueError

        Example:
            >>> my_instance = MailSender(
            ...     "sender@email.com",
            ...     "pass_sender",
            ...     "receiver@email.com",
            ...     "subject",
            ...     "text_message",
            ...     "<div>html_message<div>",
            ... )
            >>> print(my_instance.email_sender)
            sender@email.com
            >>> my_instance.email_sender = "new_email_valid@email.com"
            >>> print(my_instance.email_sender)
            new_email_valid@email.com
            >>> my_instance.email_sender = "invalid_email"
            Traceback:
                ValueError: The sender mail is not valid mail. Given: invalid_email
        """
        return self._email_sender

    @email_sender.setter
    def email_sender(self, value: str):
        if IS_EMAIL()(value)[1] is None:
            self._email_sender = value
        else:
            raise ValueError("The sender mail is not valid mail. Given: {0}".format(value))

    @property
    def email_receiver(self) -> str:
        """Get ot Set the email receiver.

        :GET:

            Get the email receiver

        :SET:
            When adding an email, it is validated, if it is not a valid email it returns a ValueError

        Example:
            >>> my_instance = MailSender(
            ...     "sender@email.com",
            ...     "pass_sender",
            ...     "receiver@email.com",
            ...     "subject",
            ...     "text_message",
            ...     "<div>html_message<div>",
            ... )
            >>> print(my_instance.email_receiver)
            receiver@email.com
            >>> my_instance.email_receiver = "new_email_valid@email.com"
            >>> print(my_instance.email_sender)
            new_email_valid@email.com
            >>> my_instance.email_sender = "invalid_email"
            Traceback:
                ValueError: The receiver mail is not valid mail. Given: invalid_email
        """
        return self._email_receiver

    @email_receiver.setter
    def email_receiver(self, value: str):
        if IS_EMAIL()(value)[1] is None:
            self._email_receiver = value
        else:
            raise ValueError("The receiver mail is not valid mail. Given: {0}".format(value))

    @property
    def alternative_sender(self) -> str:
        """The alternative sender is optional, it is the reply email.
        :GET:

            Get the alternative sender

        :SET:

            When adding an email, it is validated, if it is not a valid email it returns a ValueError
        """
        return self._alternative_sender

    @alternative_sender.setter
    def alternative_sender(self, value: str):
        if value is not None:
            if IS_EMAIL()(value)[1] is None:
                self._alternative_sender = value
            else:
                raise ValueError("The alternative mail is not valid mail. Given: {0}".format(value))
        else:
            self._alternative_sender = None

    def send(self):
        """This method sends the email that was generated.
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.alternative_sender or self.email_sender
        message["To"] = self.email_receiver
        text = MIMEText(self.text_message, "plain")
        html = MIMEText(self.html_message, "html")
        message.attach(text)
        message.attach(html)
        if self.use_ssl:
            host = smtplib.SMTP_SSL(self.server, self.port)
        else:
            host = smtplib.SMTP(self.server, self.port)
        if self.use_tls:
            host.starttls()

        host.login(self.email_sender, self.password_sender)
        host.sendmail(
            self.email_sender, self.email_receiver, message.as_string()
        )
