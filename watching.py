"""
Title: XmlConstructor

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

Tools that can be used in PhanterPWA.
"""
import os

if __name__ == '__main__':
    from phanterpwa.tools import WatchingFiles

    ins = WatchingFiles(
        os.path.normpath("C:\\GitHub\\phanterpwa\\phanterpwa"),
        os.path.normpath("C:\\Virtualenv\\py37\\phanterpwaenv\\Lib\\site-packages\\phanterpwa"),
        ignore_paths=["__pycache__", "www"]
    )
    ins.monitoring()