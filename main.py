import datetime
import json
import os

import click
import tweepy

import settings as s


def get_access():
    """Set up the Twitter API with the given access credentials."""
    auth = tweepy.OAuthHandler(s.CONSUMER_KEY, s.CONSUMER_SEC)
    api = None
    try:
        auth.set_access_token(s.ACCESS_TOK, s.ACCESS_SEC)
        api = tweepy.API(
            auth,
            parser=tweepy.parsers.JSONParser(),
            wait_on_rate_limit=True
        )
    except tweepy.TweepError as e:
        click.echo(e)
    finally:
        return api


def set_output_path():
    """Set the output filename."""
    mainpath = os.path.join(os.getcwd(), s.OUTDIR)
    if not os.path.exists(mainpath):
        os.makedirs(mainpath)
    
    filedate = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    filepath = os.path.join(mainpath, s.OUTFILE + filedate)
    return filepath


def get_tweets(api, user, count):
    """Get *count* number of tweets from given user."""
    count = count if count else 200
    total_count = api.get_user(user)['statuses_count']
    count = total_count if total_count < count else count
    data = []
    
    with click.progressbar(length=count,
                           label='{:15}'.format(user)) as bar:
        data = api.user_timeline(screen_name=user, count=count)
        if not data:
            raise ValueError(
                'No tweet data available for {}'.format(user)
            )
        ntweets = len(data)
        
        while True:
            bar.update(ntweets)
            if ntweets >= count:
                break
            else:
                max_id = data[-1]['id'] - 1
                data += api.user_timeline(
                    screen_name=user,
                    count=count - len(data),
                    max_id=max_id
                )
                ntweets = len(data)
    return data


def set_users(username):
    """Returns screen names from command line or file."""
    users = []
    if username:
        users = [u for u in username]
    else:
        with open('userlist.txt', 'r') as f:
            users = [u.strip() for u in f.readlines()]
        
        if not users:
            raise ValueError('No user specified.')
    
    return users


@click.command()
@click.argument('user', nargs=-1)
@click.option('-n', '--count', default=50,
              help='Number of tweets to get')
def run(user, count):
    """Handles script flow."""
    data = []
    click.echo('\nAuthorizing')
    api = get_access()
    if api is not None:
        users = set_users(user)
        
        click.echo(
            'Extracting tweet data from {} users'.format(len(users))
        )
        for user in users:
            try:
                tweets = get_tweets(api=api, user=user, count=count)
                data += tweets
            except Exception as e:
                click.echo(e)
                click.echo('Skipped {}'.format(user))
    
        if not data:
            click.echo('Unable to obtain tweet data for any user.')
        else:
            click.echo('Finished')
            with open(set_output_path() + '.json', 'w') as fh:
                json.dump(data, fh, indent=2)
                click.echo(
                    "Saved to '{}'".format(os.path.split(fh.name)[-1])
                )
