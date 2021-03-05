import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
        Set Config variables for the flask app.
        using environment variables where available,
        otherwise create the config variable if not done already.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'new Secret Key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turns off notification messages from the sqlalchemy db
    