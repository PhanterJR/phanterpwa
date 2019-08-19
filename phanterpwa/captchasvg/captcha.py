# -*- coding: utf-8 -*-
import random
import os
import json
from glob import glob
from phanterpwa.helpers import DIV, XML, SVG, SPAN
from phanterpwa.i18n import Translator
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serialize,
    BadSignature,
    SignatureExpired
)
__dirname__ = os.path.dirname(__file__)


class Captcha(object):
    def __init__(self,
        _id,
        secret_key,
        time_token_expire,
        num_opt=4,
        question="Which figure below corresponds to: {option}.",
        debug=False,
        translator=None):
        super(Captcha, self).__init__()
        self.debug = debug
        self.secret_key = secret_key
        self.time_token_expire = time_token_expire
        self.serializer = Serialize(
            self.secret_key,
            self.time_token_expire
        )

        self._background_color = {
            "red": "#990000",
            "yellow": "#FFCC00",
            "blue": "#6699FF"
        }
        self._foreground_color = {
            "black": "#1F1A17",
            "white": "white",
            "green": "#009933"
        }

        self._signature = None
        self._choice = None
        self.translator = translator
        self.color_pairs = dict()
        self.options = dict()
        self._opt = []
        self.recipes = dict()
        self.classification = set()
        self.vectors = dict()
        self.grafical_forms = dict()
        self.svg_forms = dict()
        self.question = question
        if isinstance(_id, str):
            self._id = _id
        else:
            raise ValueError("The captcha id must be string. Given: {0}".format(type(_id)))
        self.num_opt = num_opt
        self.keys_attributes = []
        self.keys_lines_cols = []
        if self.debug or not os.path.exists(os.path.join(__dirname__, "captchadata.json")):
            self._combine_colors()
            self._recipes()
            self._vectors()
            self._svgs()
        else:
            with open(os.path.join(__dirname__, "captchadata.json"), "r", encoding="utf-8") as f:
                captchadata = json.load(f)
                self.options = captchadata[0]
                self.grafical_forms = captchadata[1]

    def _combine_colors(self):
        cont_b = 0
        sass = ""
        for x in self._background_color:
            cont_f = 0
            self.options[x] = x
            t_sass = ""
            cont_b += 1
            t_sass_0 = "".join(["    .fil0\n        fill: ", self._background_color[x], "\n"])
            for y in self._foreground_color:
                self.options[y] = y
                cont_f += 1
                t_sass_1 = "".join([
                    t_sass,
                    "    .fil1\n        fill: ",
                    self._foreground_color[y],
                    "\n",
                    " " * 8,
                    "fill-rule: nonzero",
                    "\n"
                ])
                t_sass = "".join([
                    ".phanterpwa-captchasvg-{0}{1}".format(
                        str(cont_b).zfill(2),
                        str(cont_f).zfill(2)
                    ),
                    "\n", t_sass_0,
                    t_sass_1
                ])
                sass = "\n".join([sass, t_sass])
                t_sass = ""
                self.color_pairs[
                    "phanterpwa-captchasvg-{0}{1}".format(
                        str(cont_b).zfill(2),
                        str(cont_f).zfill(2)
                    )
                ] = [x, y]
        with open(os.path.join(__dirname__, "sass", "captcha.sass"), "w", encoding="utf-8") as f:
            f.write(sass)

    def _recipes(self):
        recs = glob(os.path.join(__dirname__, "recipes", "*.recs"))
        for x in recs:
            with open(x, "r", encoding="utf-8") as f:
                basename = os.path.basename(x)[:-5]
                self.options[basename] = basename
                self.recipes[basename] = str(f.read())

    def _vectors(self):

        clas = glob(os.path.join(__dirname__, "vectors", "*"))
        for x in clas:
            if os.path.isdir(x):
                classification_name = os.path.split(x)[-1]
                self.classification.add(classification_name)
                self.options[classification_name] = classification_name
                vecs = glob(os.path.join(x, "*.recs"))
                for v in vecs:
                    with open(v, "r", encoding="utf-8") as f:
                        basename = os.path.basename(v)[:-5]
                        self.options[basename] = basename
                        self.vectors[(classification_name, basename)] = str(f.read())

    def _svgs(self):
        code = 0
        for c in self.color_pairs.keys():
            for r in self.recipes:
                for v in self.vectors:
                    code += 1
                    self.grafical_forms[code] = list(self.color_pairs[c])
                    self.grafical_forms[code].append(r)
                    self.grafical_forms[code].append(v[0])
                    self.grafical_forms[code].append(v[1])
                    self.grafical_forms[code].append(c)
        with open(os.path.join(__dirname__, "captchadata.json"), "w", encoding="utf-8") as f:
            json.dump([self.options, self.grafical_forms], f, ensure_ascii=True, indent=2)

    @property
    def option(self):
        if not self._option:
            self._choicer()
        return self._option

    @property
    def choice(self):
        if not self._choice:
            self._choicer()
        return self._choice

    @property
    def signature(self):
        if not self._signature:
            self._choicer()
        return self._signature

    def _choicer(self):
        self.keys_attributes = [x for x in self.options.keys()] +\
            [x[1] for x in self.vectors.keys()] +\
            [x[1] for x in self.vectors.keys()]
        self.keys_lines_cols = [x for x in self.grafical_forms.keys()]
        count_attr = len(self.keys_attributes)
        choice = self.keys_attributes[random.randint(0, count_attr - 1)]
        self._choice = choice
        self._opt = []
        random.shuffle(self.keys_lines_cols)
        cont_err = 0
        cont_ok = 0
        self._option = None
        for x in self.keys_lines_cols:
            t_choice = self.grafical_forms[x][:-1]
            if choice in t_choice:
                if cont_ok == 0:
                    self._opt.append(x)
                    self._option = x
                    cont_ok += 1
            else:
                if cont_err < self.num_opt - 1:
                    self._opt.append(x)
                    cont_err += 1
                else:
                    if cont_ok == 1:
                        break
        random.shuffle(self._opt)
        sign_captha = self.serializer.dumps({
            'id_form': self._id,
            'choice': choice,
            'option': self._option
        })
        self._signature = sign_captha.decode("utf-8")

    def check(self, signature, option):
        read_signature = None
        try:
            read_signature = self.serializer.loads(signature)
        except BadSignature:
            read_signature = None
        except SignatureExpired:
            read_signature = None
        else:
            try:
                read_option = self.serializer.loads(option)
            except BadSignature:
                read_option = None
            except SignatureExpired:
                read_option = None
            else:
                if read_option and read_signature:
                    if read_signature['choice'] in self.grafical_forms[str(read_option['option'])][:-1] and\
                        read_signature['id_form'] == self._id:
                        return True
                    else:
                        return False
        return False

    @property
    def html(self):
        question = self.question
        choice = self.choice
        new_dict_t = dict()
        opt = self.options[choice]
        if isinstance(self.translator, Translator):
            for d in self.translator.languages:
                t = self.translator.translator(question, d)
                new_dict_t[d] = {
                    question.format(option=opt): t.format(option=self.translator.translator(opt, d))
                }
            question = SPAN(question.format(option=opt), _phanterpwa_i18n=new_dict_t)
        else:
            question = question.format(option=opt)
        content = []
        if self.debug:
            token_question = choice
        else:
            token_question = self.signature
        for x in self._opt:
            attrs = {
                "_xmlns": "http://www.w3.org/2000/svg",
                "_xml:space": "preserve",
                "_width": "50px",
                "_height": "50px",
                "_style": "shape-rendering:geometricPrecision; text-rendering:geometricPrecision; " +
                    "image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd",
                "_viewBox": "0 0 50 50",
                "_xmlns:xlink": "http://www.w3.org/1999/xlink",
            }
            svg_e = self.grafical_forms[x]
            recipe = svg_e[2]
            sub_folder = svg_e[3]
            vector = svg_e[4]
            attrs["_class"] = svg_e[5]
            svg_recipe = ""
            svg_vector = ""
            if self.debug:
                token_option = str(x)
            else:
                sign_option = self.serializer.dumps({
                    'option': str(x)
                })
                token_option = sign_option.decode("utf-8")
            p = os.path.join(__dirname__, "recipes", "{0}.recs".format(recipe))
            with open(p, 'r', encoding='utf-8') as f:
                svg_recipe = f.read()
            p = os.path.join(__dirname__, "vectors", sub_folder, "{0}.recs".format(vector))
            with open(p, 'r', encoding='utf-8') as f:
                svg_vector = f.read()
            content.append(
                DIV(
                    DIV(
                        DIV(
                            SVG(XML(svg_recipe), XML(svg_vector), **attrs),
                            _class='captcha-option-svg'),
                        _class='captcha-option link',
                        _token_option=token_option,
                        _token_question=token_question,
                        _id_captcha=self._id
                    ),
                    _class='captcha-option-container')
            )
        html = DIV(
            DIV(
                XML(question),
                _class='captcha-question-container'),
            DIV(
                *content,
                _class='captcha-options-container'),
            _class='captcha-container')
        html.sass_file(os.path.join(__dirname__, "sass", "captcha.sass"))
        self._html = html
        return self._html

    @property
    def html_ok(self):
        self._html_ok = DIV(
            DIV(
                XML("".join(['<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" '
                    'height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision;',
                    ' image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50"',
                    ' xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25.1541" cy="25.1175" ',
                    'r="24.5529"/><polygon class="fil1" points="14.6544,18.9408 20.4585,26.0181 39.3804,13.6859'
                    ' 43.962,20.7361 21.8877,35.1224 18.7388,37.1752 16.3517,34.266 8.16404,24.2795 "/></svg>'])),
                _class="captcha-ok-svg-container", _id="captcha-ok-svg-container-{0}".format(self._id)),
            _class='captcha-container')
        return self._html_ok


if __name__ == '__main__':
    captcha = Captcha("form", "teste", 5000)
    print(captcha.choice)
    print(captcha.html)
