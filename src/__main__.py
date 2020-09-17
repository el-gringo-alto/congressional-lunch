import datetime
import json
import os
import time

from bs4 import BeautifulSoup, SoupStrainer
import markovify
import requests
import tweepy


def twitter():
    with open('keys/twitter_api_keys.json') as f:
        keys = json.load(f)
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



def mk_house_file():
    api = twitter()

    with requests.get('https://www.house.gov/representatives') as r:
        soup = BeautifulSoup(r.text, 'lxml', parse_only=SoupStrainer(id='by-state'))

    tables = soup.find_all('table')

    reps = []

    for table in tables:
        for body in table.find_all('tbody'):
            for tr in body.find_all('tr'):
                name_container = tr.find(class_='views-field-text-3')
                name = name_container.find('a').string.split(',')
                name = f"{name[1].strip()} {name[0].strip()}"

                party = tr.find(class_='views-field-text-5').get_text(strip=True)
                if party == 'R':
                    party = 'Republican'
                elif party == 'D':
                    party = 'Democrat'
                elif party == 'L':
                    party = 'Libertarian'
                elif party == 'I':
                    party = 'Independent'

                committees_container = tr.find(class_='views-field-text-9')
                committees = []
                for li in committees_container.find_all('li'):
                    committees.append(li.get_text(strip=True))


                # get twitter accounts
                users = api.search_users(name)

                verified_users = []
                for user in users:
                    if user.verified:
                        verified_users.append(f"https://twitter.com/{user.screen_name}")

                print('Name: {}\n{}'.format(name, '\n'.join(verified_users)))

                reps.append({
                    'name': name,
                    'state': table.find('caption').get_text(strip=True),
                    'district': tr.find(class_='views-field-text-1').get_text(strip=True),
                    'party': party,
                    'committees': committees,
                    'social-media': {
                        'twitter': verified_users
                    }
                })

    with open('house.json', 'w') as f:
        json.dump(reps, f, indent=4)



def tweets_filename(chamber, party):
    dir = 'data'
    if not os.path.exists(dir):
        os.mkdir(dir)

    dir += f"/{datetime.datetime.now().strftime('%Y-%m-%d')}"

    if not os.path.exists(dir):
        os.mkdir(dir)

    if chamber == None:
        dir += '/congress_'
    else:
        dir += f"/{chamber.lower()}_"

    if party == None:
        dir += 'all'
    else:
        dir += party.lower()

    return dir + '.json'


def get_tweets(chamber=None, party=None, count_per_user=20):
    api = twitter()

    # get all the twitter urls into a list
    with open(f'{chamber.lower()}.json') as f:
        profiles = json.load(f)
    twitter_urls = []
    for profile in profiles:
        for url in profile['social-media']['twitter']:
            if party == None or profile['party'].lower() == party.lower():
                twitter_urls.append(url)


    tweets = []
    for url in twitter_urls:
        username = url.split('https://twitter.com/', 1)[1]
        try:
            page = api.user_timeline(username, tweet_mode='extended', count=count_per_user)
        except:
            print(f"Skipping @{username}")
            continue
        print(f"Grabbing {len(page)} tweets from @{username}")
        for tweet in page:
            tweets.append(tweet.full_text)
        time.sleep(1)

    with open(tweets_filename(chamber, party), 'w') as file:
        file.write(json.dumps(tweets))

    print(f"{len(tweets)} tweets scraped from {len(twitter_urls)} accounts")


def generate_text(chamber=None, party=None):
    tweets_file = tweets_filename(chamber, party)
    # scrape tweets if it hasn't been done yet
    if not os.path.exists(tweets_file):
        get_tweets(chamber, party)
    with open(tweets_file) as file:
        tweets = json.load(file)

    text_model = markovify.Text(' '.join(tweets), state_size=2)
    sentence = text_model.make_short_sentence(280)

    print(sentence)



if __name__ == '__main__':
    # mk_house_file()
    # get_tweets('house', 'republican')
    generate_text('house', 'republican')
