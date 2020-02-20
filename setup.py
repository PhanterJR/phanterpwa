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
    packages=[
        'phanterpwa',
        'phanterpwa/captchasvg',
        'phanterpwa/captchasvg/recipes',
        'phanterpwa/captchasvg/sass',
        'phanterpwa/captchasvg/vectors/',
        'phanterpwa/captchasvg/vectors/animal',
        'phanterpwa/captchasvg/vectors/arrow',
        'phanterpwa/captchasvg/vectors/number',
        'phanterpwa/captchasvg/vectors/letter',
        'phanterpwa/captchasvg/vectors/mean_of_transport',
        'phanterpwa/components',
        'phanterpwa/decorators',
        'phanterpwa/gallery',
        'phanterpwa/i18n',
        'phanterpwa/interface',
        'phanterpwa/samples',
        'phanterpwa/scaffolds',
        'phanterpwa/apitools',
        'phanterpwa/apptools',
        'phanterpwa/apptools/components'
    ],
    entry_points={
        "console_scripts": [
            "phanterpwa = phanterpwa.__main__:main",
        ],
    },
    install_requires=[
        'psutil', 'tornado', 'libsass', 'transcrypt',
        'pillow', 'itsdangerous',
        'pydal>=19.04', 'passlib'
    ],
    dependency_links=[
        'git+https://github.com/web2py/pydal.git',
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
