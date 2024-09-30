from celery import Celery
from flask import current_app as app

celery = Celery("Bakend Jobs", broker='redis://localhost:6379/0')

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
