import sass
import os
from phanterpwa.helpers import (
    DIV,
    HTML,
    HEAD,
    BODY,
    META,
    TITLE,
    SPAN,
    XML,
    STYLE,
    TABLE,
    TBODY,
    THEAD,
    TR,
    TH,
    TD,
    P,
    BR,
    CONCATENATE
)

http_equiv = {
    "_http-equiv": "Content-Type",
    "_content": "text/html; charset=UTF-8"
}

css = ""
with open(os.path.join(os.path.dirname(__file__), "email.sass"), "r") as f:
    c = f.read()
    css = sass.compile(string=c, indented=True, output_style="compressed")


html = HTML(
    HEAD(
        TITLE("{{app_name}}"),
        META(**http_equiv),
        META(
            _name="viewport",
            _content="width=device-width"
        ),
        STYLE(css)
    ),
    BODY(
        SPAN(
            "Your two factor verification code at {{app_name}}",
            " is {{code}}.",
            _class="preheader"
        ),
        TABLE(
            TR(
                TD(
                    XML("&nbsp;")
                ),
                TD(
                    DIV(
                        TABLE(
                            TR(
                                TD(
                                    TABLE(
                                        TR(
                                            TD(
                                                P("Greetings {{user_name}},"),
                                                P("An account in the application {{app_name}} linked to this email tried to login, to complete the authentication it is necessary to add this code."),
                                                TABLE(
                                                    TR(
                                                        TD(
                                                            TABLE(
                                                                TBODY(
                                                                    TR(
                                                                        TD(
                                                                            DIV("{{code}}", _class="code")
                                                                        ),
                                                                    ),
                                                                ),
                                                                _role="presentation",
                                                                _border="0",
                                                                _cellpadding="0",
                                                                _cellspacing="0",
                                                            ),
                                                            _align="center"
                                                        ),
                                                    ),
                                                    _role="presentation",
                                                    _border="0",
                                                    _cellpadding="0",
                                                    _cellspacing="0",
                                                    _class="btn btn-primary"
                                                ),
                                                P("The code will expire in {{time_expires}} after sending."),
                                                P("If it was not you, you do not need to do anything, but it is advisable to change your password. Below the login information."),
                                                TABLE(
                                                    TR(
                                                        TD(
                                                            TABLE(
                                                                THEAD(
                                                                    TR(
                                                                        TH("Field"),
                                                                        TH("Value")
                                                                    )
                                                                ),
                                                                TBODY(
                                                                    TR(
                                                                        TH(
                                                                            SPAN("IP Address")
                                                                        ),
                                                                        TD(
                                                                            SPAN("{{user_ip}}")
                                                                        )
                                                                    ),
                                                                    TR(
                                                                        TH(
                                                                            SPAN("User Agent")
                                                                        ),
                                                                        TD(
                                                                            SPAN("{{user_agent}}")
                                                                        )
                                                                    ),
                                                                ),
                                                                _role="presentation",
                                                                _border="0",
                                                                _cellpadding="0",
                                                                _cellspacing="0",
                                                            ),
                                                            _align="center"
                                                        ),
                                                    ),
                                                    _role="presentation",
                                                    _border="0",
                                                    _cellpadding="0",
                                                    _cellspacing="0",
                                                    _class="btn btn-primary"
                                                ),
                                                P("Thanks for listening! Goodbye!"),
                                            ),
                                        ),
                                        _role="presentation",
                                        _border="0",
                                        _cellpadding="0",
                                        _cellspacing="0"
                                    ),
                                    _class="wrapper"
                                ),
                            ),
                            _role="presentation",
                            _class="main"
                        ),
                        DIV(
                            TABLE(
                                TR(
                                    TD(
                                        SPAN(
                                            "{{copyright}}",
                                            _class="apple-link"
                                        ),
                                        BR(),
                                        XML("Do you like this app? <a href=\"{{link_to_your_page}}\">visit our page!</a>."),
                                        _class="content-block",
                                    )
                                ),
                                _role="presentation",
                                _border="0",
                                _cellpadding="0",
                                _cellspacing="0"
                            ),
                            _class="footer"
                        ),
                        _class="content"
                    ),
                    _class="container"
                ),
                TD(XML("&nbsp;")),
            ),
            _role="presentation",
            _border="0",
            _cellpadding="0",
            _cellspacing="0",
            _class="body"
        )
    )
)
text = CONCATENATE(
    "Greetings {{user_name}},",
    "\n\n",
    "An account in the application {{app_name}} linked to this email tried to login, to complete the authentication it is necessary to add this code.",
    "\n\n",
    "{{code}}",
    "\n\n",
    "The code will expire in {{time_expires}} after sending, if it expires, do not worry, you can request another one.",
    "\n",
    "Thank you! Bye!",
    "\n\n",
    "{{copyright}}",
    "\n",
    "{{link_to_your_page}}"
)
