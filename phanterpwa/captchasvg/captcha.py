# -*- coding: utf-8 -*-
import random
import os
from glob import glob
from phanterpwa.helpers import DIV, XML, SVG


class Captcha(object):
    def __init__(self, _id, token="", num_opt=4, question="Which figure below corresponds to: %s.", debug=False):
        super(Captcha, self).__init__()
        self.debug = debug
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
        self.color_pairs = dict()
        self.attributes = dict()
        self.recipes = dict()
        self.classification = set()
        self.vectors = dict()
        self.grafical_forms = dict()
        self.svg_forms = dict()
        self._combine_colors()
        self._recipes()
        self._vectors()
        self._svgs()
        self.question = question
        self._id = _id
        self.token = token
        self.keys_attributes = [x for x in self.attributes.keys()] +\
            [x[1] for x in self.vectors.keys()] +\
            [x[1] for x in self.vectors.keys()]
        self.keys_lines_cols = [x for x in self.grafical_forms.keys()]
        self.num_opt = num_opt
        self._choicer()

    def _combine_colors(self):
        cont_b = 0
        sass = ""
        for x in self._background_color:
            cont_f = 0
            self.attributes[x] = x
            t_sass = ""
            cont_b += 1
            t_sass_0 = "".join(["    .fil0\n        fill: ", self._background_color[x], "\n"])
            for y in self._foreground_color:
                self.attributes[y] = y
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
                t_sass = "".join([".phanterpwa-captchasvg-%s%s" %
                    (str(cont_b).zfill(2), str(cont_f).zfill(2)), "\n", t_sass_0, t_sass_1])
                sass = "\n".join([sass, t_sass])
                t_sass = ""
                self.color_pairs["phanterpwa-captchasvg-%s%s" %
                    (str(cont_b).zfill(2), str(cont_f).zfill(2))] = [x, y]
        with open(os.path.join(os.path.dirname(__file__), "sass", "captcha.sass"), "w", encoding="utf-8") as f:
            f.write(sass)

    def _recipes(self):
        recs = glob(os.path.join(os.path.dirname(__file__), "recipes", "*.recs"))
        for x in recs:
            with open(x, "r", encoding="utf-8") as f:
                basename = os.path.basename(x)[:-5]
                self.attributes[basename] = basename
                self.recipes[basename] = str(f.read())

    def _vectors(self):

        clas = glob(os.path.join(os.path.dirname(__file__), "vectors", "*"))
        for x in clas:
            if os.path.isdir(x):
                classification_name = os.path.split(x)[-1]
                self.classification.add(classification_name)
                self.attributes[classification_name] = classification_name
                vecs = glob(os.path.join(x, "*.recs"))
                for v in vecs:
                    with open(v, "r", encoding="utf-8") as f:
                        basename = os.path.basename(v)[:-5]
                        self.attributes[basename] = basename
                        self.vectors[(classification_name, basename)] = str(f.read())

    def _svgs(self):
        code = 0
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
        for c in self.color_pairs.keys():
            for r in self.recipes:
                for v in self.vectors:
                    code += 1
                    self.grafical_forms[code] = list(self.color_pairs[c])
                    self.grafical_forms[code].append(r)
                    attrs["_class"] = c
                    self.svg_forms[code] = SVG(XML(self.recipes[r]), XML(self.vectors[v]), **attrs)
                    self.grafical_forms[code].append(v[0])
                    self.grafical_forms[code].append(v[1])

    @property
    def choice(self):
        return self._choice

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def _choicer(self):
        count_attr = len(self.keys_attributes)
        choice = self.keys_attributes[random.randint(0, count_attr - 1)]
        self._choice = choice

    def check(self, attribute, number):
        try:
            number = int(number)
        except ValueError:
            return False
        if attribute in self.grafical_forms[number]:
            return True
        else:
            return False

    @property
    def html(self):
        question = self.question
        num_opt = self.num_opt
        choice = self.choice
        options = []
        random.shuffle(self.keys_lines_cols)
        cont_err = 0
        cont_ok = 0
        for x in self.keys_lines_cols:
            t_choice = self.grafical_forms[x]
            if choice in t_choice:
                if cont_ok == 0:
                    options.append(x)
                    cont_ok += 1
            else:
                if cont_err < num_opt - 1:
                    options.append(x)
                    cont_err += 1
                else:
                    if cont_ok == 1:
                        break
        random.shuffle(options)
        question = question % self.attributes[choice]
        content = []
        if self.token:
            token = self.token
        else:
            token = choice
        for x in options:
            content.append(
                DIV(
                    DIV(
                        DIV(
                            self.svg_forms[x],
                            _class='captcha-option-svg'),
                        _class='captcha-option link', _cmd_option=str(x), _token=token, _id_captcha=self._id),
                    _class='captcha-option-container')
            )
        html = DIV(
            DIV(
                question,
                _class='captcha-question-container'),
            DIV(
                *content,
                _class='captcha-options-container'),
            _class='captcha-container')
        self._html = html
        return self._html

    @property
    def html_ok(self):
        self._html_ok = DIV(
            DIV(
                XML('<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25.1541" cy="25.1175" r="24.5529"/><polygon class="fil1" points="14.6544,18.9408 20.4585,26.0181 39.3804,13.6859 43.962,20.7361 21.8877,35.1224 18.7388,37.1752 16.3517,34.266 8.16404,24.2795 "/></svg>'),
                _class="captcha-ok-svg-container", _id="captcha-ok-svg-container-%s" % (self._id)),
            _class='captcha-container')
        return self._html_ok


if __name__ == '__main__':
    for x in range(10):
        captcha = Captcha("teste")
        captcha.token = '----------------------------------------------'
        for x in captcha.svg_forms:
            with open('%s.svg' %x, 'w', encoding="utf-8") as f:
                f.write(captcha.svg_forms[x].xml().replace("&#58;",":"))


