from celery import Celery

from at_tracker.celery import config


celery_app = Celery("worker",
                    backend=config.backend,
                    broker=config.backend)

celery_app.config_from_object('at_tracker.celery.config')
