class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lmsv2.db'
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = 'super-secret-key'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'