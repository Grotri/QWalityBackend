from flask_caching import Cache
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()
cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",  # in-memory cache
    "CACHE_DEFAULT_TIMEOUT": 300  # 5 минут по умолчанию
})
