import datetime
import json
import os
import random

import markovify
import tweepy


def tweets_filename(chamber, party):
    if not os.path.exists('data'):
        os.mkdir('data')

    date = datetime.datetime.now().strftime('%Y-%m-%d')

    if not os.path.exists(f'data/{date}'):
        os.mkdir(f'data/{date}')

    if chamber == None:
        chamber_name = 'all'
    else:
        chamber_name = chamber.lower()

    if party == None:
        party_name = 'all'
    else:
        party_name = party.lower()

    return f'data/{date}/{chamber_name}_{party_name}.json'


def get_tweets(party=None, count_per_user=20):
    # connect to twitter
    with open('keys/twitter_api_keys.json') as f:
        keys = json.load(f)
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    # get all the twitter urls into a list
    with open('senate.json') as f:
        profiles = json.load(f)
    twitter_urls = []
    for profile in profiles:
        for url in profile['social-media']['twitter']:
            if party == None or profile['party'].lower() == party.lower():
                twitter_urls.append(url)


    tweets = []
    for url in twitter_urls:
        # print(f'getting {url}')
        username = url.split('https://twitter.com/', 1)[1]
        page = api.user_timeline(username, tweet_mode='extended', count=count_per_user)
        print(f'Grabbing {len(page)} tweets from @{username}')
        for tweet in page:
            tweets.append(tweet.full_text)


    with open(tweets_filename('senate', party), 'w') as file:
        file.write(json.dumps(tweets))

    print(f"{len(tweets)} tweets scraped")


def generate_text(party=None):
    with open(tweets_filename('senate', party), 'r') as file:
        tweets = json.load(file)

    # state_size = random.randint(1,3)
    text_model = markovify.Text(' '.join(tweets), state_size=2)
    sentence = text_model.make_short_sentence(280)

    # print(f'State size: {state_size}')
    print(sentence)



if __name__ == '__main__':
    get_tweets('democrat')

    # generate_text()
