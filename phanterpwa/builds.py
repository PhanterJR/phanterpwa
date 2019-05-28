# -*- coding: utf-8 -*-
import os
from .xmlconstructor import XmlConstructor


class BuildViews(object):

    def __init__(self, name, view, folder):
        super(BuildViews, self).__init__()
        self.name = name
        self.view = view
        self.folder = folder

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        if not os.path.exists(os.path.join(value)):
            try:
                os.makedirs(os.path.join(value), exist_ok=True)
            except OSError as e:
                raise e("Problem on create folder '%s'." % os.path.join(value))
        self._folder = os.path.join(value)

    def build(self):
        if isinstance(self.view, XmlConstructor):
            with open(
                os.path.join(self._folder, self.name),
                "wt",
                encoding="utf-8"
            ) as f:
                f.write(self.view.xml())
        else:
            raise TypeError("The view must be a XmlConstructor instance")
