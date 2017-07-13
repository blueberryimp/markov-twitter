import os
import sys
from random import choice
import twitter

api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

     
# print api.VerifyCredentials()

def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
    key = choice(chains.keys())
    words = [key[0], key[1]]
    #max([len(word) for word in words]) --> calculating the max len of the of words in our list (our sentece)
    while key in chains and len(" ".join(words)) <= 140 - max([len(word) for word in words]): 
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)
      
    return " ".join(words)

def tweet(tweet_msg):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    
    status = api.PostUpdate(tweet_msg)
    print status.text
        

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)
while True:
    tweet_msg = make_text(chains)
    # Your task is to write a new function tweet, that will take chains as input
    tweet(tweet_msg)
    while True: #making sure the user enters q or enter
        user_input = raw_input("Enter to tweet again [q to quit] > ")
        if user_input == 'q' or user_input =="": #"" == enter
            break
        print "q or Enter"
    if user_input.lower() == 'q':
        break
