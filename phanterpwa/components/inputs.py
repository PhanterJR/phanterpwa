from ..helpers import (
    DIV,
    LABEL,
    INPUT,
    I,
    # SPAN,
    # TEXTAREA,
    # SELECT,
    # OPTION,
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

        if "_class" in attributes:
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
                DIV(error,
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
                DIV(error,
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
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "text"
        attributes_container = {}
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)


class InputPassword(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "password"
        attributes_container = {}
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)


class InputHidden(BASEINPUT):
    def __init__(
        self,
        name: "Name of input element",
        label: "Label of the element",
        error: "Message error on validation"=None,
        style: "Css framework style (materializecss or bootstrap)"="materializecss",
        **attributes: "Attributes of input element. The key must stats with underline (_)."):
        input_type = "hidden"
        attributes_container = {"_style": "display: none;"}
        BASEINPUT.__init__(self, name, label, error, style, input_type, attributes_container, **attributes)
