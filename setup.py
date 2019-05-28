import setuptools

from phanterpwa import __version__

with open("README.md", "r") as f:
    long_description = f.read()

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
    packages=['phanterpwa'],
    install_requires=[
        'psutil', 'libsass', 'transcrypt', 'livereload', 'flask',
        'pillow', 'flask_restful', 'flask_mail', 'flask_cors', 'itsdangerous'
    ],
    dependency_links=[
        'https://github.com/web2py/pydal/archive/master.zip',
    ],
    include_package_data=True,
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
