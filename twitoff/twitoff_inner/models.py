from flask_sqlalchemy import SQLAlchemy

# create a DB object
# opening up the db connection
DB = SQLAlchemy()


# create table in the db
# using a python Class

class User(DB.Model):
    # for the different columns in our db, 
    # each one will be its own attribute on the Class

    # id column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False) #nullable=False

    # username column schema
    username = DB.Column(DB.String, nullable=False) # nullable=False

    # newest tweed id schema
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.username)


class Tweet(DB.Model):

    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False) #nullable=False

    text = DB.Column(DB.Unicode(300)) # nullable=False

    # word embeddings (vect) schema
    vect = DB.Column(DB.PickleType, nullable=False) # allows us to store np array


    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id')) # nullable=False

    # set up relationship between tweets and IDs
    # this will automatically add a new id to both the tweet 
    # and the user

    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)
    # adds a list of tweets automatically ---------------^

    # include {{user.tweets[0].text}}
    # under username/id in html file

    # tweepy - env variables - store passwords etc securely

    # spacy - NLP tools, word embeddings

    # python-dotenv - reads any key-value pairs from a .env file 
    # and sets them as environment variables in the app
    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

