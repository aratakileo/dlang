try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PACKAGE_NAME = ROOT_DIR = 'dlang'


setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    packages=[ROOT_DIR],
    url=f'https://github.com/teacondemns/{PACKAGE_NAME}',
    license='GPL-3.0',
    author='Tea Condemns',
    author_email='tea.condemns@gmail.com',
    description='Module for convenient localization/translation of the interface'
)
