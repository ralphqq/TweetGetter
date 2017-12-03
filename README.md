# TweetGetter
This script obtains a specified number of a Twitter user's (or multiple users') most recent tweets, then saves the output as a JSON file.

## Requirements
This runs on Python 2.7 and uses [tweepy 3.5.0](https://pypi.python.org/pypi/tweepy/3.5.0). Just `pip install tweepy` before running the script.

## Usage
Just cd to the project's root directory and run:

```
    $ python get-tweets.py -u screenname -n 100
```

## Options
To obtain the `n` most recent tweets from a given user, use the `-u` option to specify the user's screen name. Use the `-n` option to indicate the number of tweets to obtain. For example, the following command gets the 100 most recent tweets from the [Hacker News](https://twitter.com/newsycombinator) twitter timeline and saves the data into an output file.

```
    $ python get-tweets.py -u @newsycombinator -n 100
```

Both of these are optional arguments. If no username is specified, the script uses the list of screen names saved in the `userlist.txt` file. Similarly, the script sets the default number of tweets to be obtained at 200, if `-n` is not specified.

## Getting Tweets from Multiple Twitter Users
This script allows you to obtain tweets from multiple users. In the `userlist.txt` file, enter the screen names of the users you want to collect tweets from. Make sure no two screen names appear on the same line. Then, just ignore `-u` when running the script.

## Output
The collected data will be saved as a JSON file in the `Output` directory of the project folder.

## Access Credentials
Enter your authorization and access credentials into the appropriate variables found in the `settings.py` file:

```
    CONSUMER_KEY = ''
    CONSUMER_SEC = ''
    ACCESS_TOK = ''
    ACCESS_SEC = ''
```

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contributing
Please contribute to this project in whatever capacity. Thanks.