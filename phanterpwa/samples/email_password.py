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
            "Use this temporary password to create a new password:",
            " {{password}}.",
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
                                                P("A new password was requested on {{app_name}}, a temporary password was sent (Expires in {{time_expires}}), use it to add a new password."),
                                                TABLE(
                                                    TR(
                                                        TD(
                                                            TABLE(
                                                                TBODY(
                                                                    TR(
                                                                        TD(
                                                                            DIV("{{password}}", _class="code")
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
                                                P("If you have not made this request, you do not have to do anything."),
                                                P("Any problem please contact support."),
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
    "A new password was requested on {{app_name}}, a temporary password was sent (Expires in {{time_expires}}), use it to add a new password.",
    "\n\n",
    "{{password}}",
    "\n\n",
    "If you have not made this request, you do not have to do anything.",
    "\n",
    "Any problem please contact support.",
    "\n\n",
    "{{copyright}}",
    "\n",
    "{{link_to_your_page}}"
)