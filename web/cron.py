'''
Crontab functions
'''
import configparser
from datetime import datetime
import json
import logging
import pathlib
import random
import re
import time

import mysql.connector
import markovify
import requests
import tweepy



keys_file = pathlib.Path('keys.ini')
congress_file = pathlib.Path('congress.json')
data_dir = pathlib.Path('data')
log_file = pathlib.Path('congressional-lunch.log')

config = configparser.ConfigParser()
config.read(keys_file)

# setup logging for when we scrape tweets
logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


# Since I only want to split this between democrats and republicans, third
# parties can with one of the two independents go with democrats because most
# of them in congress caucus with the democrats.
third_parties = {
    'Republican': ['Libertarian', 'New Progressive'],
    'Democratic': ['Independent']
}


def data_file_path(party, data_type):
    """
    Return a file path for either the file containing the Markov corpus or the
    likes and retweets data.
    """
    party_dir = data_dir / party.lower()
    if not party_dir.exists():
        party_dir.mkdir(parents=True)

    if data_type.lower() == 'tweets':
        return party_dir / 'tweets.json'
    elif data_type.lower() == 'data':
        return party_dir / 'data.json'
    else:
        raise Exception(f"{data_type} is not a valid file. Please specify 'tweets' or 'data'.")


def cleanup_congress(*handles: str):
    """
    Remove usernames from the congress file.
    """
    with congress_file.open(encoding='utf-8') as file:
        profiles = json.load(file)

    for handle in handles:
        removed = False
        for profile in profiles:
            for username in profile['twitter']:
                if handle.lower() == username.lower():
                    profile['twitter'].remove(username)

                    print(f"Removed @{handle} from {profile['name']} ({profile['party']})")

                    removed = True
                    break
            if removed:
                break
        else:
            print(f"Unable to find @{handle}")

    with congress_file.open('w', encoding='utf-8') as file:
        json.dump(profiles, file, indent=4)



def scrape_data():
    """
    Pull the tweets from each congressman and save the markov chain to a file
    corresponding to their party.
    """
    # connect to the twitter api
    twitter_keys = config['twitter']
    auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
    auth.set_access_token(twitter_keys['access_token'], twitter_keys['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    for party in ['Republican', 'Democratic']:
        # get all the twitter urls into a list
        with congress_file.open(encoding='utf-8') as file:
            profiles = json.load(file)
        usernames = []
        for profile in profiles:
            if (profile['party'] == party or
            # libertarians go with republicans because
            # there's not enough of them for a whole dataset
            profile['party'] in third_parties['Republican'] and
            party == 'Republican' or
            # independents go with democratics
            # for the same reason as above
            profile['party'] in third_parties['Democratic'] and
            party == 'Democratic'):
                for username in profile['twitter']:
                    usernames.append(username)

        # set date from a week ago so we can separate tweets
        week_ago_timestamp = datetime.now().timestamp() - 604800

        tweets_within_week = []
        tweets_outside_week = []
        retweets = []
        likes = []
        for username in usernames:
            try:
                page = api.user_timeline(screen_name=username, tweet_mode='extended')
            except tweepy.TweepyException as exc:
                print(f"Skipping @{username} - {exc}")
                logging.info(f"@{username} - {exc}", )
                continue
            print(f"Grabbing {len(page)} tweets from @{username}")
            for tweet in page:
                if tweet.created_at.timestamp() > week_ago_timestamp:
                    tweets_within_week.append(tweet.full_text)
                else:
                    tweets_outside_week.append(tweet.full_text)
                # get likes and retweets from retweeted status or likes will be 0
                if hasattr(tweet, 'retweeted_status'):
                    retweets.append(tweet.retweeted_status.retweet_count)
                    likes.append(tweet.retweeted_status.favorite_count)
                else:
                    retweets.append(tweet.retweet_count)
                    likes.append(tweet.favorite_count)
            # have it wait so we don't rate limit the api
            time.sleep(2)

        data = {
            'retweets': retweets,
            'likes': likes
        }

        tweets_within_model = markovify.Text(' '.join(tweets_within_week), retain_original=False)
        tweets_outside_model = markovify.Text(' '.join(tweets_outside_week), retain_original=False)
        # place 75% more weight on tweets made within the week
        combined_model = markovify.combine([tweets_within_model, tweets_outside_model], [1.75, 1])
        combined_model.compile(inplace=True)

        tweets_file = data_file_path(party, 'tweets')
        tweets_file.write_text(combined_model.to_json())

        data_file = data_file_path(party, 'data')
        data_file.write_text(json.dumps(data))

        print(f"{len(tweets_within_week) + len(tweets_outside_week)} tweets scraped from {len(usernames)} {party} accounts")



def gen_tweet():
    """
    Create all the data for the tweet and upload it to the database.
    """
    with congress_file.open(encoding='utf-8') as file:
        congress = json.load(file)

    # get a random congressman
    congressman = random.choice(congress)
    if congressman['party'] in third_parties['Republican']:
        party = 'Republican'
    elif congressman['party'] in third_parties['Democratic']:
        party = 'Democratic'
    else:
        party = congressman['party']

    # generate sentences until one doesn't contain a twitter link nor ellipsis
    tweets_file = data_file_path(party, 'tweets')
    text_model = markovify.Text.from_json(tweets_file.read_text())
    good_sentence = False
    while not good_sentence:
        sentence = text_model.make_short_sentence(280)
        if not re.search('(https:\/\/t\.co\/\S*)|(…)|(^\d*\/\d*)', sentence):
            good_sentence = True

    name = congressman['name']
    handle = random.choice(congressman['twitter'])

    # get retweets and likes based on an existing one
    # i should make this into a tuple at some point when scraping
    data_file = data_file_path(party, 'data')
    with data_file.open(encoding='utf-8') as file:
        data = json.load(file)
    data_idx = random.randint(0, len(data['retweets']))
    retweets = data['retweets'][data_idx]
    likes = data['likes'][data_idx]

    cur_time = datetime.now().strftime('%I:%M %p')
    cur_date = datetime.now().strftime('%b %d, %Y')

    with mysql.connector.connect(**config['database'], raise_on_warnings=False) as db:
        with db.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id INT NOT NULL AUTO_INCREMENT,
                    tweet TEXT NOT NULL,
                    name TEXT NOT NULL,
                    handle TEXT NOT NULL,
                    party TEXT NOT NULL,
                    retweets INT,
                    likes INT,
                    time TEXT,
                    date TEXT,
                    PRIMARY KEY (id)
                )
            """)

            cur.execute('''INSERT INTO tweets
                    (tweet, name, handle, party, retweets, likes, time, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (sentence, name, handle, party, retweets, likes, cur_time, cur_date))
            db.commit()

    print(f"""{'-' * 15}
Tweet: {sentence}
Name: {name}
Handle: @{handle}
Party: {party}
Retweets: {retweets}
Likes: {likes}
Time: {cur_time}
Date: {cur_date}
{'-' * 15}""")
