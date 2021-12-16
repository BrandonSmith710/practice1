from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user, get_all_usernames #TWITTER
import tweepy 
from os import getenv
from .predict import predict_user

# create a factory for serving up the app when it is launched
def create_app():

    # initializes flask app
    app = Flask(__name__)

    #configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # connect our db to our app object

    DB.init_app(app)

    @app.before_first_request
    def create_tables():
        DB.create_all()

    # Make our 'home' or 'root' route
    @app.route('/')
    def root():
        # do this when someone hits the home page
        return render_template('base.html', title='Home', users=User.query.all())
        

    # get app.route('/reset') here
    
    @app.route('/update')
    def update():
        usernames = get_all_usernames()
        # users = User.query.all()
        # usernames = [user.username for user in users]
        for uname in usernames:
            add_or_update_user(uname)
        return 'All users have been updated.'

    

    @app.route("/reset")
    def reset():                #<-- 10:43
        # create user for db, import user class and connection

        # removes everything from db
        DB.drop_all()
        # create new db with indicated columns
        DB.create_all()
        # create user

        # DB.session.add()
        # save the db

        # tweet1 = Tweet(id=1, text='this is some tweet text', user=brandon)
        # tweet2 = Tweet(id=2, text='some more tweet text', user=julian)
        # tweet3 = Tweet(id=1, text='my second tweet is happening now', user=brandon)
        # tweet4 = Tweet(id=2, text='julian has made his second tweet', user=julian)
        # tweet5 = Tweet(id=1, text='this will be my final tweet', user=brandon)
        # tweet6 = Tweet(id=2, text='julian is done tweeting now too', user=julian)

        # for x in [tweet1,tweet2,tweet3,tweet4,tweet5,tweet6]:
        #     DB.session.add(x)

        # for a_tweet in all_tweets:
        #     new = Tweet(id = twitter_user.id, text=a_tweet.full_text, user=nytimes)
        #     DB.session.add(new)

        # id --> elon['twitter_handle']['id'] for REQUESTS

        # DB.session.commit()

        # # display new user on the page
        # # query to get all users
        # users = User.query.all()
        return render_template('base.html', title='Reset Database')
        # return render_template('base.html', users=users) #title='test'

    @app.route('/user', methods=['POST'])
    @app.route('/user/<names>', methods=['GET'])
    def user(name=None, message=''):

        name = name or request.values['user_name']

        try:

            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User "{name}" was successfully added'
            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []

        else:
            return render_template('user.html', title=name, tweets=tweets,
            message=message)



    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare a user to themselves'
        else:
            tweet_text = request.values['tweet_text']
            prediction = predict_user(user0, user1, tweet_text)
            message = '''"{}" is more likely to have been said
                          by {} than {}'''.format(tweet_text,
                              user1 if prediction else user0,
                              user0 if prediction else user1 
            )
        return render_template('prediction.html', title='Prediction',
        message=message)
    return app


# export FLASK_APP=twitoff_inner

# flask run