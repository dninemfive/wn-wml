# from https://www.turing.com/kb/how-to-create-pypi-packages
from setuptools import setup, find_packages

setup(
    name='warno-mod-framework',
    version='0.0.0',
    author='dninemfive',
    author_email='me@dninemfive.com',
    description='Modding framework for WARNO',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)