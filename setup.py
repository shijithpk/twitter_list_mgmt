import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='twitter_list_mgmt',
    version='0.1',
    description='Python library for Twitter list management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shijithpk/twitter-list-management',
    author='Shijith Kunhitty',
    author_email='mail@shijith.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='twitter, lists, lifehack, lifehacker',
    packages=['twitter_list_mgmt'],
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=[
        'tweepy==3.8.0',
        'pandas==1.2.3'
    ],
    project_urls={
         'Source': 'https://github.com/shijithpk/twitter-list-management'
    },
)