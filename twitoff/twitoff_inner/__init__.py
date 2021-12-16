from .app import create_app

# telling flask to use our create_app factory
# now app will be named "APP"
APP = create_app()


# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Tweet=Tweet)