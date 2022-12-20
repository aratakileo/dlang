try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dlang',
    version='0.0.1',
    packages=['dlang'],
    url='https://github.com/teacondemns/dlang',
    install_requires=[],
    license='GPL-3.0',
    author='Tea Condemns',
    author_email='tea.condemns@gmail.com',
    description='Module for convenient localization of the interface'
)
