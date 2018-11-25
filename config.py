import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://team:paris@localhost:3306/hotel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
