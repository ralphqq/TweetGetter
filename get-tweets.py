# The script for extracting tweets

import argparse
import datetime
import json
import os
import sys

import tweepy

import settings as s


def get_access():
    """Set up the Twitter API with the given access credentials."""
    auth = tweepy.OAuthHandler(s.CONSUMER_KEY, s.CONSUMER_SEC)
    auth.set_access_token(s.ACCESS_TOK, s.ACCESS_SEC)
    api = tweepy.API(
        auth,
        parser=tweepy.parsers.JSONParser(),
        wait_on_rate_limit=True
    )
    return api


def set_output_path():
    """Set the output filename."""
    mainpath = os.path.join(os.getcwd(), s.OUTDIR)
    if not os.path.exists(mainpath):
        os.makedirs(mainpath)
    
    filedate = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    filepath = os.path.join(mainpath, s.OUTFILE + filedate)
    
    return filepath


def show_progress(ntweets=0, loop='initial'):
    """Shows the tweet collection progress"""
    offset = {'initial': 0, 'subsequent': 23}
    report = '{} tweets obtained'.format(ntweets)
    sys.stdout.write('\b' * offset[loop] + '{:23}'.format(report))
    

def get_tweets(api, user, count):
    """Get *count* number of tweets from given user."""
    count = count if count else 200
    data = []
    data = api.user_timeline(screen_name=user, count=count)
    
    while True:
        ntweets = len(data)
        show_progress(ntweets, 'subsequent')
        if ntweets >= count:
            break
        else:
            max_id = data[-1]['id'] - 1
            data += api.user_timeline(
                screen_name=user,
                count=count - len(data),
                max_id=max_id
            )
    
    return data


def set_users(username):
    """Returns screen names from command line or file."""
    users = []
    if username:
        users.append(username)
    else:
        with open('userlist.txt', 'r') as f:
            users = [u.strip() for u in f.readlines()]
        
        if not users:
            raise ValueError('No user specified.')
    
    return users


def main(args):
    """Handles script flow."""
    print '\nAuthorizing'
    api = get_access()
    data = []
    
    users = set_users(args.user)
    
    print 'Extracting tweet data from %d users' % len(users)
    
    for user in users:
        sys.stdout.write('- Now processing %s: ' % user)
        show_progress()
        tweets = get_tweets(api=api, user=user, count=args.numtweets)
        data += tweets
        sys.stdout.write('\n')
    
    with open(set_output_path() + '.json', 'w') as fh:
        json.dump(data, fh, indent=1)
        print 'Saved data to file %s' % os.path.split(fh.name)[-1]
    
    print 'Finished\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',
                        help='Screen name of target Twitter user.')
    parser.add_argument('-n', '--numtweets',
                        help='How many tweets to retrieve.', type=int)
    
    try:
        main(parser.parse_args())
    except Exception as e:
        print '\a%s' % e
