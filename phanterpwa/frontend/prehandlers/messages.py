import phanterpwa.frontend.gatehandler as gatehandler
import phanterpwa.frontend.decorators as decorators
import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.components.left_bar as left_bar
import phanterpwa.frontend.preloaders as preloaders
import phanterpwa.frontend.components.widgets as widgets
import phanterpwa.frontend.forms as forms
import phanterpwa.frontend.components.modal as modal
from org.transcrypt.stubs.browser import __pragma__

__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = sessionStorage = JSON = M = js_undefined = window = setTimeout = document = console = this = \
    __new__ = FormData = console = localStorage = 0
__pragma__('noskip')

DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
H2 = helpers.XmlConstructor.tagger("h2")
FORM = helpers.XmlConstructor.tagger("form")
SPAN = helpers.XmlConstructor.tagger("span")
IMG = helpers.XmlConstructor.tagger("img", True)
INPUT = helpers.XmlConstructor.tagger("input", True)
A = helpers.XmlConstructor.tagger("A")
OPTION = helpers.XmlConstructor.tagger("option")
SELECT = helpers.XmlConstructor.tagger("select")
UL = helpers.XmlConstructor.tagger("ul")
LI = helpers.XmlConstructor.tagger("li")
STRONG = helpers.XmlConstructor.tagger("strong")
XTABLE = widgets.Table
XML = helpers.XML
XTRD = widgets.TableData
XTRH = widgets.TableHead
XFOOTER = widgets.TableFooterPagination
I18N = helpers.I18N
CONCATENATE = helpers.CONCATENATE

__pragma__('kwargs')


class Messages(gatehandler.Handler):
    @decorators.check_authorization(lambda: window.PhanterPWA.get_auth_user() is not None)
    def initialize(self):
        arg0 = self.request.get_arg(0)
        arg1 = self.request.get_arg(1)
        arg2 = self.request.get_arg(2)
        if arg0 == "inbox":
            html = CONCATENATE(
                DIV(
                    DIV(
                        DIV(
                            DIV(I18N("MESSAGES", **{'pt-BR': "MENSAGENS"}), _class="phanterpwa-breadcrumb"),
                            DIV(I18N("INBOX", **{'pt-BR': "CAIXA DE ENTRADA"}), _class="phanterpwa-breadcrumb"),
                            _class="phanterpwa-breadcrumb-wrapper"
                        ),
                        _class="p-container"),
                    _class='title_page_container card'
                ),
                DIV(
                    DIV(
                        DIV(
                            DIV(preloaders.android, _style="width: 300px; height: 300px; overflow: hidden; margin: auto;"),
                            _style="text-align:center; padding: 50px 0;"
                        ),
                        _id="content-users",
                        _class='p-row card e-padding_20'
                    ),

                    _class="phanterpwa-container p-container"
                ),
            )
            html.html_to("#main-container")
            self.get_messages()

    def get_messages(self):
        window.PhanterPWA.GET(
            "api",
            "messages"
            "inbox",
            onComplete=self.after_get_messages
        )

    def after_get_messages(self, data, ajax_status):
        if ajax_status == "success":
            json = data.responseJSON
            table = TABLE(
                TR(
                    TH(
                        I18N("Sender", {"_pt-BR": "Remetente"})
                    ),
                    TH(
                        I18N("Subject", {"_pt-BR": "Assunto"})
                    ),
                    TH(
                        I18N("Datetime", {"_pt-BR": "Dia e Hora"})
                    ),
                ),
                _class="phanterpwa-messages-table"
            )
            for x in json.internal_messages:
                _class="phanterpwa-messages-table-line "
                readed = x.internal_messages_recipients.message_read
                if str(readed).lower() == "true":
                    _class="phanterpwa-messages-table-line no-read"
                sender = DIV(
                    "{0} {1}".format(x.auth_user.first_name, x.auth_user.last_name),
                    SPAN("<", x.auth_user.email, ">", _class="phanterpwa-messages-table-email"),
                    **{
                        "_title": x.auth_user.email,
                        "_data-id_auth_user": x.auth_user.id,
                        "_data-email": x.auth_user.email,
                    }
                )
                date_and_time = x.internal_messages.send_on
                subject = DIV(x.internal_messages.subject, _class="phanterpwa-messages-table-subject")
                table.append(
                    TR(
                        TD(
                            sender
                        ),
                        TD(
                            subject
                        ),
                        TD(
                            date_and_time
                        ),
                        _class=_class
                    )
                )


__pragma__('nokwargs')
