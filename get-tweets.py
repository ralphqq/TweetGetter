# The script for extracting tweets

import argparse
import datetime
import json
import os

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
    

def get_tweets(api, user, count):
    """Get *count* number of tweets from given user."""
    count = count if count else 200
    data = []
    data = api.user_timeline(screen_name=user, count=count)
    
    if count > 200:
        
        while len(data) < count:
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
    print '\nAuthorizing...'
    api = get_access()
    data = []
    
    users = set_users(args.user)
    
    print 'Extracting tweets from %d users...' % len(users)
    
    for user in users:
        print ' - Now processing %s' % user
        tweets = get_tweets(api=api, user=user, count=args.numtweets)
        data += tweets
        print '    - Obtained %d tweets from %s' % (len(tweets), user) 
    
    with open(set_output_path() + '.json', 'w') as fh:
        json.dump(data, fh, indent=1)
    
    print 'Finished...'


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
