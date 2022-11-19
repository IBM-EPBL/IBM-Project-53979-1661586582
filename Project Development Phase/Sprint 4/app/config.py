import ibm_db

class Config:
    
    NEWS_BASE_URL_SOURCES = 'https://newsapi.org/v2/top-headlines/sources?apiKey={}'
    NEWS_BASE_EVERYTHING_URL = 'https://newsapi.org/v2/everything?domains={}&apiKey={}'
    NEWS_BASE_HEADLINES_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'
    NEWS_BASE_SOURCE = 'https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'
    API_KEY = "ccee2e6628404b82b42f3c2b43026b5f"

class DB:
    DB_URI = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=jqk44878;PWD=q4Y1FZWLAnlINU5j",'','')

class SendGridMailConfig:
    SECRET_KEY = 'ramharidhra'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USERNAME = 'News Tracker'
    MAIL_PASSWORD = 'yssjwgzycdagtngl'
    MAIL_DEFAULT_SENDER = 'parakeetevening@gmail.com'

class App:
    SECRET_KEY = 'ramharidhra'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True


config_options= {
    'development': DevConfig,
    'production': ProdConfig
}