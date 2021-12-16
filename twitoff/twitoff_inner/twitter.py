# from os import getenv
# import tweepy
import requests, ast
from .models import DB, Tweet, User
import spacy


# key = getenv('TWITTER_API_KEY')
# secret = getenv('TWITTER_API_KEY_SECRET')


# TWITTER_AUTH = tweepy.OAuthHandler(key, secret)

# TWITTER = tweepy.API(TWITTER_AUTH)

# add new user to db if they dont already exist
# if the user does already exist, just grab their most
# recent tweets that we don't already have and add them to db

def add_or_update_user(username):
    '''Takes username and pulls over and tweet date from
    the Twitter API. The data should get added to db'''

    try:
        HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'
        # twitter_user = TWITTER.get_user(screen_name=username)
        
        # getting info from james' app
        user = ast.literal_eval(requests.get(HEROKU_URL+username).text)
        # create db user from my db model
        # check if user already exists
        # use existing user if exists, otherwise create user
        # db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id,
        # username=username))

        if User.query.get(user['twitter_handle']['id']):

            db_user = User.query.get(user['twitter_handle']['id'])
        else:
            db_user = User(id=user['twitter_handle']['id'], username=user['twitter_handle']['username'])

            DB.session.add(db_user)

        tweets = user['tweets']

                                        # 200 - retweets - replies
        # tweets = twitter_user.timeline(count=200, exclude_replies=True,
        # include_rts=False, tweet_mode='extended',
        # since_id=db_user.newest_tweet_id)

        # check if newest tweet in db is same as newest from twitter API,
        # if they are same, no need to add. Otherwise, add the newest tweets
        # that haven't been saved

        if tweets:
            db_user.newest_tweet_id = tweets[0]['id']

        # need to check if tweet is already in db & skip if so

        # get our word embeddings and put in db
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet['full_text'])
            db_tweet = Tweet(id=tweet['id'],
                             text=tweet['full_text'][:300],
                             vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)


    except Exception as e:
        # shows what went wrong if needed
        print(f'Error Processing {username}: {e}')
        raise e
    else:
    # save the user and all of the tweets that were added to the db session

        DB.session.commit()


nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

# 10:30am

def get_all_usernames():
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)
    return usernames
# len(user.tweets)

# user = User.query.all()

# word embedding - list of numbers - unique encoding for 
# how that word/ combo of words tends to be used in the
# english language


# ensure export FLASK_APP=app.py

# $ python -m spacy download en_core_web_sm
# flask shell


# >>> import spacy                          # 10:51
# >>> nlp = spacy.load('en_core_web_sm')
# >>> len(nlp('a string of text').vector)
# >>> nlp('Bloomtech is the best school ever').vector

# >>> nlp.to_disk('my_model') # creates new folder with nlp tools


