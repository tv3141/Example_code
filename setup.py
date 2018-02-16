from setuptools import setup

setup(
    name='download_files',
    version='2016-11-29',
    install_requires=[
        'requests>=2.7.0',
    ],
    entry_points='''
        [console_scripts]
        download_files=download_files:main
    ''',
)
