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
    TR,
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
            "Your activation code at {{app_name}}",
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
                                                P("You have created an account on {{app_name}}, we are happy about it, but there is still one step left: confirmation of your email, this is possible using the confirmation code below that will be requested in the application."),
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
                                                P("The code will expire in {{time_expires}} after sending, if it expires, do not worry, you can request another one."),
                                                P("Thank you for your trust! Bye!"),
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
    "You have created an account on {{app_name}}, we are happy about it, but there is still one step left: confirmation of your email, this is possible using the confirmation code below that will be requested in the application.",
    "\n\n",
    "{{code}}",
    "\n\n",
    "The code will expire in {{time_expires}} after sending, if it expires, do not worry, you can request another one.",
    "\n",
    "Thank you for your trust! Bye!",
    "\n\n",
    "{{copyright}}",
    "\n",
    "{{link_to_your_page}}"
)
