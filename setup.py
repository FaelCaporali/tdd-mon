from setuptools import setup, find_packages
import os


version = open("VERSION").read()

setup(
    name='tdd-pytest-monitor',
    version=version,
    author='Fael Caporali',
    author_email='faelcaporalidev@gmail.com',
    url='https://github.com/FaelCaporali/tdd-pmon',
    description='Simple script to automate running tests on files changes and simplify test driven design',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(exclude="tests"),
    install_requires=[
        'pytest',
        'pytest-xdist'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tdd-mon = src.main:main'],
    },    
)