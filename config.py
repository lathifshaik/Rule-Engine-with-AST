class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rules.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # Optional, for additional security
