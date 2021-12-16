import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):

    '''
    Determine and return which user is more likely to say a given tweet
    '''

    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()


    # get np array of word embeddings for each user's tweets
    user0_vect = np.array([tweet.vect for tweet in user0.tweets])
    user1_vect = np.array([tweet.vect for tweet in user1.tweets])

    # use vstack to concatenate two-dimensional numpy arrays
    # x matrix
    vects = np.vstack([user0_vect, user1_vect])

    # np.concatenate to concat one-dimensional numpy arrays
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))
    # y vector
    labels = np.concatenate([zeros, ones])

    # train a regression
    log_reg = LogisticRegression()
    log_reg.fit(vects, labels)

    # get prediction
    # vectorize the hypothetical text parameter
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # must pass in 2d array [hypo_tweet_vect]
    prediction = log_reg.predict([hypo_tweet_vect])

    return prediction.reshape(1, -1)



# print(predict_user('ryanallred', 'nasa', 'the rocket is going to the moon'))



    