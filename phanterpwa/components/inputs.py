from ..helpers import (
    DIV,
    LABEL,
    INPUT,
    I,
    # SPAN,
    TEXTAREA,
    SELECT,
    OPTION,
    # CONCATENATE,
    # UL,
    # LI,
    # A
)
from ..xmlconstructor import XmlConstructor


class BASEINPUT(XmlConstructor):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        input_type: "type of input"="text",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):

        attributes["_type"] = input_type
        attributes["_name"] = name
        if "_id" not in attributes:
            attributes["_id"] = "phanterpwa-input-%s" % name

        if "_title" not in attributes:
            attributes["_title"] = label
        attrs_container = {
            "_id": "phanterpwa-container-input-text-%s" % name,
            "_class": "phanterpwa-container-input-text phanterpwa-flag-%s" % style,
            "_phanterpwa-css_style": style,
            "_phanterpwa-input_name": name,
            "_phanterpwa-input_id": attributes["_id"],
        }
        if attributes_container:
            for x in attributes_container:
                if x == "_class":
                    attrs_container["_class"] = "phanterpwa-container-input-text phanterpwa-flag-%s %s" %\
                        (style, attributes_container[x])
                else:
                    attrs_container[x] = attributes_container[x]

        label_attr = {"_for": attributes["_id"]}

        if "_phanterpwa_languages" in attributes:
            label_attr['_phanterpwa_languages'] = attributes["_phanterpwa_languages"]
            attributes["_phanterpwa_languages"] = None

        if "_class" in attributes and attributes["_class"]:
            new_class = "form-control {0}".format(attributes["_class"].strip())
            if style == "bootstrap":
                new_class = " ".join([attributes["_class"].strip(), "form-control"])
            attributes["_class"] = new_class
        else:
            attributes["_class"] = "form-control"
        self.input = INPUT(
            **attributes
        )
        if style == "materializecss":
            new_content = [
                DIV(I(_class="fas fa-check"),
                    _id="phanterpwa-input-check-%s" % name,
                    _class="phanterpwa-input-check"),
                DIV(
                    self.input,
                    LABEL(
                        label,
                        **label_attr),
                    _class="input-field"),
                DIV(error if error else "",
                    _title=error,
                    _id="phanterpwa-materialize-input-error-%s" % name,
                    _class="phanterpwa-materialize-input-error"),
            ]
        elif style == "bootstrap":
            new_content = [
                DIV(I(_class="fas fa-check"),
                    _id="phanterpwa-input-check-%s" % name,
                    _class="phanterpwa-input-check"),
                DIV(
                    LABEL(
                        label,
                        **label_attr),
                    self.input,
                    _class="form-group"),
                DIV(error if error else "",
                    _title=error,
                    _id="phanterpwa-materialize-input-error-%s" % name,
                    _class="phanterpwa-materialize-input-error"),
            ]
        else:
            raise ValueError("The style must be materializecss or bootstrap. given: %s" % style)
        XmlConstructor.__init__(self, 'div', False, *new_content, **attrs_container)


class InputTextarea(XmlConstructor):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        input_type: "type of input"="text",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):

        attributes["_type"] = input_type
        attributes["_name"] = name
        if "_id" not in attributes:
            attributes["_id"] = "phanterpwa-input-%s" % name

        if "_title" not in attributes:
            attributes["_title"] = label
        attrs_container = {
            "_id": "phanterpwa-container-input-text-%s" % name,
            "_class": "phanterpwa-container-input-text phanterpwa-flag-%s" % style,
            "_phanterpwa-css_style": style,
            "_phanterpwa-input_name": name,
            "_phanterpwa-input_id": attributes["_id"],
        }
        if attributes_container:
            for x in attributes_container:
                if x == "_class":
                    attrs_container["_class"] = "phanterpwa-container-input-text phanterpwa-flag-%s %s" %\
                        (style, attributes_container[x])
                else:
                    attrs_container[x] = attributes_container[x]

        label_attr = {"_for": attributes["_id"]}

        if "_phanterpwa_languages" in attributes:
            label_attr['_phanterpwa_languages'] = attributes["_phanterpwa_languages"]
            attributes["_phanterpwa_languages"] = None
        if style == "materializecss":
            if "_class" in attributes and attributes["_class"]:
                new_class = " ".join([attributes["_class"].strip(), "materialize-textarea"])
                attributes["_class"] = new_class
            else:
                attributes["_class"] = "materialize-textarea"

        elif style == "bootstrap":
            attributes["_rows"]
            if "_class" in attributes and attributes["_class"]:
                new_class = " ".join([attributes["_class"].strip(), "form-control"])
                attributes["_class"] = new_class
            else:
                attributes["_class"] = "form-control"
            if "_rows" not in attributes and attributes["_class"]:
                attributes["_rows"] = "3"

        self.input = TEXTAREA(
            **attributes
        )
        if style == "materializecss":
            new_content = [
                DIV(I(_class="fas fa-check"),
                    _id="phanterpwa-input-check-%s" % name,
                    _class="phanterpwa-input-check"),
                DIV(
                    self.input,
                    LABEL(
                        label,
                        **label_attr),
                    _class="input-field"),
                DIV(error if error else "",
                    _title=error,
                    _id="phanterpwa-materialize-input-error-%s" % name,
                    _class="phanterpwa-materialize-input-error"),
            ]
        elif style == "bootstrap":
            new_content = [
                DIV(I(_class="fas fa-check"),
                    _id="phanterpwa-input-check-%s" % name,
                    _class="phanterpwa-input-check"),
                DIV(
                    LABEL(
                        label,
                        **label_attr),
                    self.input,
                    _class="form-group"),
                DIV(error if error else "",
                    _title=error,
                    _id="phanterpwa-materialize-input-error-%s" % name,
                    _class="phanterpwa-materialize-input-error"),
            ]
        else:
            raise ValueError("The style must be materializecss or bootstrap. given: %s" % style)
        XmlConstructor.__init__(self, 'div', False, *new_content, **attrs_container)


class InputText(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "text"
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)


class InputSelect(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        placeholder="",
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "text"
        attributes['_phanterpwa-input-select'] = name
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)


class InputPassword(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "password"
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)


class InputHidden(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "hidden"
        if "_style" not in attributes_container:
            attributes_container["_style"] = "display: none;"
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)


class InputTextAndButton(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        icon: "Button Icon"=I(_class='fas fa-yin-yang'),
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "text"
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)
        old_content = self.content
        self.content = [
            DIV(
                old_content,
                DIV(
                    icon,
                    _id='phanterpwa_input_icon_button_{0}'.format(name),
                    _class='btn phanterpwa_input_icon_button'),
                _class="phanterpwa_input_icon_button_container"
            )
        ]


class InputSelectAndButton(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        icon: "Button Icon"=I(_class='fas fa-yin-yang'),
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "text"
        attributes['_phanterpwa-input-select'] = name
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)
        old_content = self.content
        self.content = [
            DIV(
                old_content,
                DIV(
                    icon,
                    _id='phanterpwa_input_icon_button_{0}'.format(name),
                    _class='btn phanterpwa_input_icon_button'),
                _class="phanterpwa_input_icon_button_container"
            )
        ]

class InputTextPlus(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        attributes_container: "Attributes of container. The key must stats with underline (_)." = {},
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "text"
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)
        old_content = self.content
        self.content = [
            DIV(
                old_content,
                DIV(
                    I(_class='fas fa-plus'),
                    _id='phanterpwa_input_plus_button_{0}'.format(name),
                    _class='btn phanterpwa_input_plus_button'),
                _class="phanterpwa_input_text_plus_container"
            )
        ]

