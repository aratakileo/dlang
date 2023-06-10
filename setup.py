try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PACKAGE_NAME = ROOT_DIR = 'dlang'


setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    packages=[ROOT_DIR, f'{ROOT_DIR}.resource'],
    package_data={ROOT_DIR: ['resource/*/*']},
    url=f'https://github.com/aratakileo/{PACKAGE_NAME}',
    license='MIT',
    author='Arataki Leo',
    author_email='aratakileo@gmail.com',
    description='Module for convenient localization/translation of the interface'
)
