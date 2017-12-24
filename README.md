# TweetGetter
This command line tool obtains data from a specified number of a Twitter user's (or multiple users') tweets, then saves the output as a JSON file for further data analysis.

## Installation
This script works on Python 2.7 and 3.6. It requires [tweepy](http://docs.tweepy.org/en/v3.5.0/) and [click](http://click.pocoo.org/5/). To install all dependencies (and to be able to execute the script as a command line tool):

1. cd to the project's root directory.
2. Create a new virtual environment.
3. Run the following command:

```
    $ pip install --editable .
```

Make sure to activate this virtual environment before using the script.

## Usage
The basic syntax goes as follows:

```
    $ tweets <screen_name1> <screen_name2> ... -n <number_of_tweets_to_get>
```

## Parameters
The command accepts an arbitrary number of screen names (@handles without the @ mark) to obtain tweet data from. If no screen name is specified, the script instead looks for screen names in the `userlist.txt` file (more on this below).

The `-n` option lets you indicate how many of the most recent tweets from each user to get. If not specified, it defaults to 200 tweets. Although you can pass any positive integer to this option, the maximum number of tweets you can obtain from a user's timeline is limited to 3,200 (see the [GET statuses/user_timeline](https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html) section of the Twitter Developers page).

For example, to collect the tweet data of the 100 most recent statuses from [Hacker News](https://twitter.com/newsycombinator):

```
    $ tweets newsycombinator -n 100
```

The following command gets the data of the 1000 most recent tweets from [Elon Musc](https://twitter.com/elonmusk) and [SpaceX](https://twitter.com/SpaceX)

```
    $ tweets elonmusk SpaceX -n 1000
```

## Getting Tweets from a List of Twitter Users
This script also allows you to obtain tweets from a list of users. In the `userlist.txt` file, save the screen names of the users you want to collect tweets from. Make sure no two screen names appear on the same line. Then, just don't specify any screen name when running the command on the terminal.

The below command gets the 500 most recent tweets from each of the users whose screen names are saved on the `userlist.txt` file:

```
    $ tweets -n 500
```

## Output
The collected data will be saved as a JSON file in the `Output` directory of the project folder.

The output JSON file contains a collection of tweet objects. Please see the [official docs for tweet objects](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object) to see the full list of attributes.

## Access Credentials
Enter your authorization and access credentials into the appropriate variables found in the [settings.py](https://raw.githubusercontent.com/ralphqq/TweetGetter/master/settings.py) file:

```
    CONSUMER_KEY = ''
    CONSUMER_SEC = ''
    ACCESS_TOK = ''
    ACCESS_SEC = ''
```

Here's a quick tutorial on [how to obtain access keys and credentials](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/).

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contributing
Please contribute to this project in whatever capacity. Thanks.