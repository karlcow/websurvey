import os
from setuptools import setup, find_packages

from survey import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = []

setup(
    name = "Web Survey",
    version = ".".join(map(str, __version__)),
    description = "",
    long_description = read('README.mdown'),
    url = '',
    license = 'MIT',
    author = 'Karl Dubost',
    author_email = 'karl+websurvey@la-grange.net',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = requirements,
    tests_require = [],
)
