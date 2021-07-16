"""
Title: XmlConstructor

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

Tools that can be used in PhanterPWA.
"""
import os

if __name__ == '__main__':
    import shutil
    from phanterpwa.tools import WatchingFiles
    dispensaveis = ["phanterpwa.egg-info", "dist", "build"]
    for x in dispensaveis:
        if os.path.isdir(x):
            try:
                shutil.rmtree(os.path.normpath(os.path.join("C:\\GitHub\\phanterpwa\\", x)))
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
                pass
            while os.path.exists(x):
                pass
    ins = WatchingFiles(
        os.path.normpath("C:\\GitHub\\phanterpwa\\phanterpwa"),
        os.path.normpath("C:\\Virtualenv\\py37\\phanterpwaenv\\Lib\\site-packages\\phanterpwa"),
        ignore_paths=["__pycache__", "www"]
    )
    ins.monitoring()
