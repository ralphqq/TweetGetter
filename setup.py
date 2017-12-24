from setuptools import setup

setup(
    name='tweetgetter',
    version='0.2',
    py_modules=['main'],
    include_package_data=True,
    install_requires=[
        'Click',
        'tweepy',
    ],
    entry_points='''
        [console_scripts]
        tweets=main:run
    ''',
)