# scrapy-mongoengine


## Usage

in your scrapu settings.py

```.python
# mongodb
MONGOENGINE_ENABLED = True
MONGODB_DATABASES = {
    "default": {
        "name": "scrapy",
        "host": "127.0.0.1",
        "password": database_password,
        "username": database_user,
        "tz_aware": True,  # if you using timezones in django (USE_TZ = True)
    }
}

MONGODB_UNIQUE_KEY = "origin_link"
MONGODB_ADD_TIMESTAMP = True
```
