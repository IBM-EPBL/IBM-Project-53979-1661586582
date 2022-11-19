import ibm_db

class Config:
    
    NEWS_BASE_URL_SOURCES = 'https://newsapi.org/v2/top-headlines/sources?apiKey={}'
    NEWS_BASE_EVERYTHING_URL = 'https://newsapi.org/v2/everything?domains={}&apiKey={}'
    NEWS_BASE_HEADLINES_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'
    NEWS_BASE_SOURCE = 'https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'
    API_KEY = "0b827eeefc5440a1bfb1d73dc65d7250"

class DB:
    DB_URI = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=jqk44878;PWD=q4Y1FZWLAnlINU5j",'','')

class SendGridMailConfig:
    SECRET_KEY = 'ramharidhra'
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'News Tracker Application'
    MAIL_PASSWORD = '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'
    MAIL_DEFAULT_SENDER = '714019104088@smartinternz.com'

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