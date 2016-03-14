from flask import Flask, has_app_context
from celery import Celery


class Celery(Celery):

    def __init__(self, *args, **kwargs):
        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'application' in kwargs:
            self.init_app(kwargs['application'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.config_from_object(app.config)