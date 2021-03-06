import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import edutalk

BASE_DIR = os.path.dirname(__file__)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_requires():
    with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
        return tuple(map(str.strip, f.readlines())) + get_backport_requires()


def get_backport_requires():
    return tuple()


def get_test_requires():
    with open(os.path.join(BASE_DIR, 'test-requirements.txt')) as f:
        return tuple(map(str.strip, f.readlines()))


def get_dep_links():
    links = []
    reqs = list(get_requires())
    for i, x in enumerate(reqs):
        if 'paho.mqtt.python' in x:
            links.append(x)
            reqs[i] = 'paho-mqtt'
    return reqs, links


REQUIRES, DEP_LINKS = get_dep_links()

setup(
    name='edutalk',
    version=edutalk.version,
    author='The EduTalk Team',
    author_email='edutalk@pcs.cs.nctu.edu.tw',
    url='https://gitlab.com/IoTtalk/edutalk/',
    packages=find_packages(exclude=['docs']),
    entry_points={
        'console_scripts': ('edutalk=edutalk.cli:main',),
    },
    data_files=[
        ('share/edutalk', ['share/edutalk.ini.sample']),
    ],
    install_requires=REQUIRES,
    dependency_links=DEP_LINKS,
    tests_require=get_test_requires(),
    cmdclass={'test': PyTest},
    platforms=['Linux', 'FreeBSD'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
