#!/usr/bin/env python3
import pathlib
import re
import sys
import os

from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
WORK_DIR = pathlib.Path(__file__).parent

if sys.version_info < (3, 6):
    raise RuntimeError("webpay requires Python 3.6+")


def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'webpay' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_description():
    """
    Read full description from 'README.rst'
    :return: description
    :rtype: str
    """
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='webpay-bahamta',
    version=get_version(),
    packages=find_packages(
        exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    include_package_data=True,
    author='AmirHossein Falahati',
    author_email='mramirho3inf@gmail.com',
    license='MIT',
    description='Python package for Webpay gateway API.',
    long_description=get_description(),
    url='https://github.com/amirho3inf/python-webpay',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'requests'
    ],
    extras_require={
        'async': [
            'aiohttp',
        ]
    }
)
