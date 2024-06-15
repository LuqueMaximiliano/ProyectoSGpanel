import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://mluken:0123456789@localhost/aml_data_base'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
