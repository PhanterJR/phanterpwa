from ..tools import config


class ProjectConfig(object):
    """docstring for ProjectConfig"""

    def __init__(self, config_file):
        super(ProjectConfig, self).__init__()
        self.config_file = config_file
        self.original = dict(**config(self.config_file))
        self.projectConfig = dict(**self.original)

    def add_item(self, i, v):
        self.projectConfig[i] = v
        config(self.config_file, {i: v})

    def __iter__(self):
        for c in self.projectConfig:
            yield c

    def __getitem__(self, i):
        return dict(**config(self.config_file, self.projectConfig))[i]

    def __setitem__(self, i, v):
        self.add_item(i, v)
