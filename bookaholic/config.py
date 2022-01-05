import os
class Config:

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    SECRET_KEY = '8bf452767368d7eb212c70163649465a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
