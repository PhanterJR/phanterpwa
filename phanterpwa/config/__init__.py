from ..tools import config


class ProjectConfig(object):
    """docstring for ProjectConfig"""

    def __init__(self, config_file):
        super(ProjectConfig, self).__init__()
        self.config_file = config_file
        self.ProjectConfig = config(self.config_file)

    def add_item(self, i, v):
        self.ProjectConfig[i] = v
        config(self.config_file)

    def __iter__(self):
        for c in self.ProjectConfig:
            yield c

    def __getitem__(self, i):
        return dict(**self.ProjectConfig)[i]

    def __setitem__(self, i, v):
        self.add_item(i, v)
