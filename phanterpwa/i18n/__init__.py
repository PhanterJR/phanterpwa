# -*- coding: utf-8 -*-
import json
import os
import glob


class Translator(object):
    """docstring for Translator"""
    instances = dict()

    def __init__(self, path, identifier, debug=False, direct_translation=None):
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
        self.direct_translation = direct_translation
        self.load()
        self.add_instance(identifier, self)

    @classmethod
    def get_instance(cls, identifier):
        return cls.instances.get(identifier, None)

    @classmethod
    def add_instance(cls, identifier, obj):
        cls.instances[identifier] = obj

    def add_language(self, lang):
        """Adds new dictionarie"""
        if not os.path.exists(os.path.join(self.path, "{0}.json".format(lang))):
            with open(os.path.join(self.path, "{0}.json".format(lang)), 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
                self._languages[lang] = {}

    def load(self):
        """Read dictionaries"""
        if os.path.isdir(self.path):
            for g in glob.glob(os.path.join(self.path, "*.json")):
                if os.path.basename(g) == "entries.json":
                    with open(g, 'r', encoding='utf-8') as f:
                        self.keys = set(json.load(f))
                else:
                    basename = os.path.basename(g)[0:-5]
                    try:
                        with open(g, 'r', encoding='utf-8') as f:
                            self._languages[basename] = json.load(f)
                    except json.decoder.JSONDecodeError as e:
                        raise Exception(e, "file: {g}")
            for l in self._languages:
                for w in self._languages[l]:
                    if w not in self.keys:
                        self.keys.add(w)
            for t in self.keys:
                for l in self._languages:
                    if t not in self._languages[l]:
                        self._languages[l][t] = t
        else:
            raise IOError("path must be a folder. give: {0}".format(self.path))

    @property
    def direct_translation(self):
        return self._direct_translation

    @direct_translation.setter
    def direct_translation(self, dictionary):
        if isinstance(dictionary, str):
            self._direct_translation = str(dictionary)
        elif dictionary is None:
            self._direct_translation = None
        else:
            raise TypeError("The dictionary of T must be a string or None. Given: {0}".format(type(dictionary)))

    def T(self, entry):
        if self.direct_translation:
            return self.translator(entry, self.direct_translation)
        else:
            return self._T(entry)

    def _T(self, entry):
        """Adds new word in all dictionaries after save if it does not exist"""
        if self.debug:
            self.load()
        if entry not in self.keys:
            self.keys.add(entry)
        for t in self.keys:
            for l in self._languages:
                if t not in self._languages[l]:
                    self._languages[l][t] = t
        if self.debug:
            self.save()
        return entry

    def save(self):
        """Save the translations in all dictionaries"""
        sorted_keys = list(self.keys)
        sorted_keys.sort()
        t_lang = {}
        for l in self._languages:
            t_lang[l] = {}
            for t in sorted_keys:
                if t not in self._languages[l]:
                    t_lang[l][t] = t
                else:
                    t_lang[l][t] = self._languages[l][t]

        with open(os.path.join(self.path, "entries.json"), 'w', encoding='utf-8') as f:
            json.dump(sorted_keys, f, ensure_ascii=False, indent=2)
        for x in self._languages:
            with open(os.path.join(self.path, "%s.json" % x), 'w', encoding='utf-8') as f:
                json.dump(t_lang[x], f, ensure_ascii=False, indent=2)

    def translate(self, dictionary, entry, translation):
        """creates a translation of a word for a specific dictionary,
        while for others hold the original word.
        If the dictionary or entry does not exist it will be created.

        @dictionary: Name of the dictionary.
        @entry: Word to be translated.
        @translation: translation of the word.

        eg.
        >>> TranlatorInstance.translate("pt-BR", "Orange", "Laranja")

        returns: {"pt-BR", {"Orange": "Laranja"}}
        This translation will be added to this specific dictionary,
        while in the other dictionary will not be changed

        """
        self._T(entry)
        if dictionary not in self._languages:
            self.add_language(dictionary)
            self._languages[dictionary] = {entry: translation}
        else:
            self._languages[dictionary][entry] = translation
        if self.debug:
            self.save()
        return {dictionary: {entry: translation}}

    def translator(self, entry, dictionary=None):
        self._T(entry)
        if dictionary and dictionary in self._languages:
            if entry in self._languages[dictionary]:
                return self._languages[dictionary][entry]
        if self.debug:
            self.save()
        return entry

    def dictionaries(self, entries=None):
        if self.debug:
            self.load()
        if entries:
            if isinstance(entries, (list, tuple)):
                langs = {}
                for l in self.languages:
                    for v in entries:
                        self._T(v)
                        if v in self.languages[l]:
                            langs[l] = {v: self.languages[l][v]}
                return langs
            elif isinstance(entries, dict):
                langs = {}
                for l in self.languages:
                    for v in entries:
                        self._T(entries[v])
                        if entries[v] in self.languages[l]:
                            if l in langs:
                                langs[l][v] = self.languages[l][entries[v]]
                            else:
                                langs[l] = {v: self.languages[l][entries[v]]}
                        else:
                            langs[l] = {v: entries[v]}
                return langs
            elif isinstance(entries, str):
                langs = {}
                for l in self.languages:
                    self._T(entries)
                    if entries in self.languages[l]:
                        langs[l] = {entries: self.languages[l][entries]}
                return langs
            else:
                return {}
        else:
            return self.languages

    def phanterpwa_i18n(self, entrie):
        if isinstance(entrie, str):
            self._T(entrie)
            langs = {}
            o_keys = list(self.languages.keys())
            o_keys.sort()
            for l in o_keys:
                if entrie in self.languages[l]:
                    if entrie != self.languages[l][entrie]:
                        langs[l] = {entrie: self.languages[l][entrie]}
            if langs:
                return langs
            return None
        else:
            raise ('The arg entrie in method phanterpwa_i18n must be String. Given: {0}'.format(type(entrie)))

    @property
    def languages(self):
        return self._languages

    def __bool__(self):
        return os.path.exists(os.path.join(self.path, "entries.json"))


def browser_language(header_language, default="en-US"):
    if header_language:
        languages = header_language.split(",")
        locales = []
        for language in languages:
            parts = language.strip().split(";")
            if len(parts) > 1 and parts[1].startswith("q="):
                try:
                    score = float(parts[1][2:])
                except (ValueError, TypeError):
                    score = 0.0
            else:
                score = 1.0
            locales.append((parts[0], score))
        if locales:
            locales.sort(key=lambda pair: pair[1], reverse=True)
            codes = [l[0] for l in locales]
            if len(codes) > 0:
                return codes[0]
    return default
