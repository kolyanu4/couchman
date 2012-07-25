import os
from setuptools import setup, find_packages

def read(fname):
    """ Return the text of the file fname """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name = "couchman",
    version = "0.4",
    description = "derived work of the Krayzman's project https://github.com/kraizman/couchman",
    author = "Nikolay Gavrilyuk",
    author_email = "nikolay.gavrilyuk@smscoin.com",
    url = "https://github.com/kolyanu4/couchman",
    packages = find_packages(),
    package_data = {
        '': ['media/*'],
    },
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'couchman = couchman.couchman:main',
        ]
    },
    long_description = read('README'),
    classifiers = [
        "Development Status :: 3 - Beta",
        "Topic :: Utilities",
        "License :: GPL License",
    ],
) 
