import os
from phanterpwa import server

projectPath = os.path.dirname(__file__)
Run = server.ProjectRunner()
Run.run(projectPath, compile=True)
