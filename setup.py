# https://www.turing.com/kb/how-to-create-pypi-packages
# https://github.com/tomchen/example_pypi_package/blob/main/setup.py
from setuptools import setup, find_packages

REPO = f'https://github.com/dninemfive/wn-mfw'
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    # basic metadata
    name='warno-mod-framework',
    author='dninemfive',
    author_email='me@dninemfive.com',
    # description
    description='Modding framework for WARNO',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=REPO,
    project_urls={
        'Bug Reports': f'{REPO}/issues',
        'Source Code': REPO
    },
    # tags
    keywords='WARNO, mod, framework, modding, Eugen Systems',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
         # not OS-independent because it runs .bat files provided by Eugen
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed'
    ],
    python_requires='>=3.10',
    # packages
    package_dir={'':'src'},
    packages=find_packages(where='src'),
)