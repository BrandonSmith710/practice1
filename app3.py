from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Day, DB
from .api import make_query


def create_app():
    app2 = Flask(__name__)
    # database filepath config
    app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    DB.init_app(app2)

    @app2.route("/")
    def root():
        for day in make_query()['consolidated_weather']:
            # add each day to database
            db_day = Day(id=day['id'],min_temp=day['min_temp'],
            max_temp=day['max_temp'],date=day['date'])
            DB.session.add(db_day)
        DB.session.commit()

        # query the db for specific day
        dec_21 = Day.query.filter(Day.date == '2021-12-21').one()

        return '\n'.join(map(str,[dec_21.id,dec_21.min_temp,
                                  dec_21.max_temp, dec_21.date]))

    

    @app2.route('/reset')
    def route():
        DB.drop_all()
        DB.create_all()

        return 'database reset'

        
    return app2
