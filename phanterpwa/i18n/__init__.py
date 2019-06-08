# -*- coding: utf-8 -*-
import json
import os
import glob


class Translator(object):
    """docstring for Translator"""

    def __init__(self, path, debug=False):
        super(Translator, self).__init__()
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        if not os.path.exists(os.path.join(path, "entries.json")):
            with open(os.path.join(path, "entries.json"), 'w', encoding='utf-8') as f:
                json.dump([], f)
        self.keys = set()
        self._languages = {}
        self.debug = debug
        self.path = path
        self.load()

    def add_language(self, lang):
        if not os.path.exists(os.path.join(self.path, "%s.json" % lang)):
            with open(os.path.join(self.path, "%s.json" % lang), 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
                self._languages[lang] = {}

    def load(self):
        if os.path.isdir(self.path):
            for g in glob.glob(os.path.join(self.path, "*.json")):
                if os.path.basename(g) == "entries.json":
                    with open(g, 'r', encoding='utf-8') as f:
                        self.keys = set(json.load(f))
                else:
                    basename = os.path.basename(g)[0:-5]
                    with open(g, 'r', encoding='utf-8') as f:
                        self._languages[basename] = json.load(f)
        else:
            raise IOError("path must be a folder. give: %s" % self.path)

    def T(self, string):
        if self.debug:
            self.load()
        if string not in self.keys:
            self.keys.add(string)
        if self.debug:
            self.save()
        return string

    def save(self):
        text = [x for x in self.keys]
        if self.debug:
            for t in text:
                for l in self._languages:
                    if t not in self._languages[l]:
                        self._languages[l][t] = t

        with open(os.path.join(self.path, "entries.json"), 'w', encoding='utf-8') as f:
            json.dump(text, f, ensure_ascii=False, indent=2)
        for x in self._languages:
            with open(os.path.join(self.path, "%s.json" % x), 'w', encoding='utf-8') as f:
                json.dump(self._languages[x], f, ensure_ascii=False, indent=2)

    def translate(self, dictionary, verbete, translation):
        self.T(verbete)
        if dictionary not in self._languages:
            self._languages[dictionary] = {verbete: translation}
        else:
            self._languages[dictionary][verbete] = translation
        if self.debug:
            self.save()
        return {dictionary: {verbete: translation}}

    def translator(self, verbete, dictionary=None):
        self.T(verbete)
        if dictionary and dictionary in self._languages:
            if verbete in self._languages[dictionary]:
                return self._languages[dictionary][verbete]
        if self.debug:
            self.save()
        return verbete

    def dictionaries(self, verbetes=None):
        if self.debug:
            self.load()
        if verbetes:
            if isinstance(verbetes, (list, tuple)):
                langs = {}
                for l in self.languages:
                    for v in verbetes:
                        if v in self.languages[l]:
                            langs[l] = {v: self.languages[l][v]}
                return langs
            elif isinstance(verbetes, dict):
                langs = {}
                for l in self.languages:
                    for v in verbetes:
                        if verbetes[v] in self.languages[l]:
                            langs[l] = {v: self.languages[l][v]}
                return langs
            elif isinstance(verbetes, str):
                langs = {}
                for l in self.languages:
                    if verbetes in self.languages[l]:
                        langs[l] = {verbetes: self.languages[l][v]}
                return langs
            else:
                return {}
        else:
            return self.languages

    @property
    def languages(self):
        return self._languages
