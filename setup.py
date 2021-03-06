
from setuptools import setup, find_packages
from venture.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='venture',
    version=VERSION,
    description='Find out what episode is streaming',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='k.ensign',
    author_email='km.ensign@gmail.com',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'venture': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        venture = venture.main:main
    """,
)
