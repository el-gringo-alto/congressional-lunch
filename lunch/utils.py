""" Contains utility functions and variables for the main functions of the
    module.
"""
import configparser
import json
import logging
import pathlib



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
