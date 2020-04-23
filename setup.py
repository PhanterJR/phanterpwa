import setuptools

from phanterpwa import (
    __version__,
    __install_requeriments__
)

with open("README.md", "r") as f:
    long_description = f.read()

def packs(exclude=[]):
    import os
    import glob
    import re
    from pathlib import PurePath
    current_dir = os.path.join(os.path.dirname(__file__), "phanterpwa")
    exclude = exclude
    packs = []
    for x in glob.glob(os.path.join(current_dir, "**"), recursive=True):
        if os.path.isdir(x) and not os.path.basename(x).startswith("_") and "." not in x:
            p = PurePath(x)
            p = p.relative_to(current_dir)
            result = os.path.join(os.path.basename(current_dir), *p.parts)
            if exclude:
                not_passed = []
                for e in exclude:
                    if callable(e):
                        if e(x):
                            not_passed.append(True)
                    elif isinstance(e, str):
                        if any(e == x or os.path.basename(x) == e or re.search(e, x)):
                            not_passed.append(True)
                if not not_passed:
                    packs.append(result.replace("\\", "/"))
            else:
                packs.append(result.replace("\\", "/"))
    return packs


def manin(exclude=[]):
    import os
    import glob
    import re
    from pathlib import PurePath
    exclude = exclude
    current_dir = os.path.join(os.path.dirname(__file__), "phanterpwa")
    files = ""
    for x in glob.glob(os.path.join(current_dir, "**"), recursive=True):
        if os.path.isfile(x) and not os.path.basename(x).endswith(".py") and "__" not in x:
            p = PurePath(x)
            p = p.relative_to(current_dir)
            result = os.path.join(os.path.basename(current_dir), *p.parts)
            if exclude:
                not_passed = []
                for e in exclude:
                    if callable(e):
                        if e(x):
                            not_passed.append(True)
                    elif isinstance(e, str):
                        if any([e == x, os.path.basename(x) == e, re.search(e, x)]):
                            not_passed.append(True)

                if not not_passed:
                    files = "".join([files, "include ", result.replace("\\", "/"), "\n"])


            else:
                files = "".join([files, "include ", result.replace("\\", "/"), "\n"])
    with open("MANIFEST.in", "w", encoding="utf-8") as f:
        f.write(files)
    return files
    
manin(exclude=["sync.ffs_db", "secret.ini", "phanterpwa.pid"])

setuptools.setup(
    name="phanterpwa",
    version=__version__,
    url='https://github.com/PhanterJR/phanterpwa',
    license='MIT',
    author='PhanterJR',
    author_email='phanterjr@conexaodidata.com.br',
    maintainer='PhanterJR',
    maintainer_email='phanterjr@conexaodidata.com.br',
    description='Tools for the phanterpwadeveloper framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[*packs()],
    entry_points={
        "console_scripts": [
            "phanterpwa = phanterpwa.__main__:main",
        ],
    },
    install_requires=__install_requeriments__,
    dependency_links=[
        'git+https://github.com/web2py/pydal.git',
    ],
    include_package_data=True,
    exclude_package_data={'': ["sync.ffs_db", "secret.ini", "phanterpwa.pid"]},
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
)
