from celery import Celery, Task

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    broker = app.config.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
    backend = app.config.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.broker_url = broker
    celery_app.conf.result_backend = backend
    celery_app.conf.timezone = "Asia/Kolkata"
    celery_app.conf.broker_connection_retry_on_startup = True
    
    # Set this as the default app so @shared_task uses it
    celery_app.set_default()
    
    # Re-finalize to pick up any pending @shared_task registrations
    celery_app.autodiscover_tasks(['application'])
    
    return celery_app