from celery.schedules import crontab

from at_tracker.common import config

backend_pass = ':{0}@'.format(config.REDIS_PASS) if config.REDIS_PASS else ''

backend = 'redis://{0}{1}:{2}/{3}'.format(backend_pass,
                                          config.REDIS_HOST,
                                          config.REDIS_PORT,
                                          config.REDIS_DB_TASKS)

imports = ('at_tracker.celery.tasks',)

task_annotations = {'*': {'rate_limit': '10/s'}}

beat_schedule = {
    'fetch_routes':{
        'task': 'at_tracker.celery.tasks.fetch_routes',
        #'schedule': crontab(minute=0, hour='*/4'),
        'schedule': 60.0,
    },
    'fetch_stops':{
        'task': 'at_tracker.celery.tasks.fetch_stops',
        #'schedule': crontab(minute=1, hour='*/4'),
        'schedule': 60.0,
    },
    'fetch_agencies':{
        'task': 'at_tracker.celery.tasks.fetch_agencies',
        #'schedule': crontab(minute=2, hour=1),
        'schedule': 60.0,
    },
    'fetch_vehicles':{
        'task': 'at_tracker.celery.tasks.fetch_vehicles',
        'schedule': 10.0,
    }
}