from phanterpwa.server import PhanterPWATornado

if __name__ == "__main__":
    import os
    projectPath = os.path.dirname(__file__)
    print(projectPath)
    AppRunv = PhanterPWATornado(projectPath)
    try:
        AppRunv.run()
    except KeyboardInterrupt:
        AppRunv.stop()
