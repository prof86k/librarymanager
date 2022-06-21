from __future__ import absolute_import
from celery import Celery
import os
from django.conf import settings

# set the default settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE','librarymanagementcore.settings')

# create celery app

app = Celery('librarymanagementcore',include=['librarymanagementcore.tasks'])
# app = Celery('tasks',broker='redis://localhost')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug(self):
    print(f'Request : {self.request}')


app.conf.update(
    result_expires = 3600,
)

if __name__ == '__main__':
    app.start()