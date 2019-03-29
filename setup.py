#!/usr/bin/env python3

# Standard library
import re

# setuptools
from setuptools import setup, find_packages

# booklib
from booklib import __version__

# Constants
IMAGES = re.compile(r'\[.*\]\(http.*\)\n',
                    flags=re.MULTILINE)

with open('README.md', encoding='utf-8') as fin:
    long_description = IMAGES.sub('', fin.read())

setup(
    name="booklib",
    version=__version__,
    description='Turn your book collection to a library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'PyQT5>=5.12.1',
        'python-dateutil>=2.8.0',
        'SQLAlchemy>=1.3.1',
    ],
    author='Alex Hartoto',
    author_email='ahartoto.dev@gmail.com',
    url='https://github.com/ahartoto/booklib',
    keywords=['book', 'library',],
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt'
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
