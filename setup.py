#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import sys
    reload(sys).setdefaultencoding("UTF-8")
except:
    pass


try:
    from setuptools import setup
except ImportError:
    print('Please install or upgrade setuptools or pip to continue')
    sys.exit(1)


import codecs


def read(filename):
    return codecs.open(filename, encoding='utf-8').read()


long_description = '\n\n'.join([read('README.md'),
                                read('AUTHORS'),
                                read('CHANGES')])

__doc__ = long_description

requirements = []


setup(name='EGDSimulator',
      description='',
      version='0.1',
      long_description=long_description,
      author='Marco Lettere',
      author_email='marco.lettere@nubisware.com',
      maintainer='Marco Lettere',
      maintainer_email='marco.lettere@nubisware.com',
      url='https://github.com/nubisware/egdsimulator',
      keywords='EGD EthernetGlobalData egdsimulator simulator',
      license='MIT License',
      install_requires=requirements,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research/Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
      packages=['egdsimulator'],
      platforms="Linux, Windows, Mac",
      use_2to3=False,
      zip_safe=False)