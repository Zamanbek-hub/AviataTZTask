# AviataTZTask
Show tickets by API provider

This task done for vacancy of [Aviata](https://aviata.kz/) <br/>

*The description of task is get data top airlines directions from [api](https://docs.kiwi.com/booking/) <br/>
then save data in cache, every midnight update data in cache, <br/> in addition every selected period time check price_change accordingly update*

## I run Django with Celery, Redis on Ubuntu Machine in Windows
Do run this you have to do:
 1. Have Linux Machine
 2. Install Python and VirtualEnv [(link)](https://www.digitalocean.com/community/tutorials/how-to-install-django-and-set-up-a-development-environment-on-ubuntu-16-04)
 3. Install Django, Celery and Redis (*pip install django celery redis*) 
 4. Install Redis server(*sudo apt install redis-serve*r)
 5. Install requirements.txt 
 6. Run Django 
 7. Run Celery: 
    1. sudo service redis-server start
    2. celery -A airlines(project_name) worker -B -l INFO
 
# Schedule to call functions for update cache, realized on Celeru.Crontab:
```
from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379'
accept_content = ['json']       # we get dates on json
task_serializer = 'json'
CELERY_BEAT_SCHEDULE = {
    'feel_cache_about_lines':{
        'task':'app.tasks.feel_cache_about_lines',
        'schedule':crontab(minute=0, hour=0),       # every midnight
    },
    'check_flight':{
        'task':'app.tasks.check_flight',
        'schedule':crontab(hour="*/1"),             # every hour
    }
}
```
 
# All the functiones that should by schedule(CELERY_BEAT_SCHEDULE) lies in file:
      app.tasks

# For Cache used Redis 
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://127.0.0.1:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "example"
    }
}

```

# For DB used:
      PostgreSql
     
 

