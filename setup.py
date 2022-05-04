#!/usr/bin/env python
from setuptools import setup


if __name__ == '__main__':
    setup(
        name='sphinx_tools',
        version='0.0.0',
        description='Sphinx tools for generating doc',
        author='Pierre Delaunay',
        packages=[
            'sphinx_tools',
            'sphinx_tools.doxygen',
        ],
        setup_requires=['setuptools'],
        install_requires=['bs4', 'breathe', 'sphinx'],
        package_data={"sphinx_tools": ['doxygen/Doxyfile.in']},
    )
