from setuptools import setup, find_packages


version = open("VERSION").read()

setup(
    name='tdd-monitor',
    version=version,
    author='Fael Caporali',
    author_email='faelcaporalidev@gmail.com',
    url='https://github.com/FaelCaporali/tdd-pmon',
    description='Simple script to automate running tests on files changes.'
    "Simplify test driven design",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest',
        'pytest-xdist'
    ],
    entry_points={
        'console_scripts': [
            'tdd-mon=tdd_monitor.src.main:main'],
    },
)
