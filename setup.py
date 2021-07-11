import pathlib
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()
long_descriptionx = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='twitter_list_mgmt',
    version='0.1.2',
    description='A Python package for managing Twitter lists',
    long_description=long_descriptionx,
    long_description_content_type='text/markdown',
    url='https://github.com/shijithpk/twitter-list-management',
    author='Shijith Kunhitty',
    author_email='mail@shijith.com',
    license='Unlicense',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='twitter, lists, lifehack, lifehacker',
    packages=['twitter_list_mgmt'],
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'tweepy>=4.0.0a0',
        'pandas>=1.2.3'
    ],
    project_urls={
         'Source': 'https://github.com/shijithpk/twitter-list-management'
    }
)