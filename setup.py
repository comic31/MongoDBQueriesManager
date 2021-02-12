import pathlib
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mongo-queries-manager',
    version='0.0.1',
    packages=find_packages(exclude=("tests", "examples")),
    url='https://github.com/comic31/MongoDBQueriesManager',
    license='MIT',
    author='Modo team',
    author_email='theodangla32@gmail.com',
    include_package_data=True,
    description='Convert query parameters from API urls to MongoDB queries !',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'dateparser>=1.0.0',
        'pymongo>=3.11.3'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Topic :: Database',
        'Topic :: System :: Networking',
        'Development Status :: 2 - Pre-Alpha',
    ],
)
