from flask import Flask
from flask_security import Security
from celery.schedules import crontab
from config import DevelopmentConfig
from application.resources import api
from application.data import datastore, cache
from application.models import db, Product
import flask_excel as excel
from flask_cors import CORS
from application.workers import celery_init_app
from application.tasks import daily_reminder, monthly_report
from celery.result import AsyncResult
from flask import jsonify, send_file
from flask_security import auth_required, roles_accepted
import time


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.security = Security(app, datastore)
    cache.init_app(app)
    with app.app_context():
        import application.views

    return app


app = create_app()
celery_app = celery_init_app(app)


@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        # Send email everyday at 8 PM
        crontab(hour=20, minute=0),
        # crontab(minute='*/1'),
        daily_reminder.s(subject="Daily Reminder"),
    )

@celery_app.on_after_configure.connect
def send_report(sender, **kwargs):
    sender.add_periodic_task(
        # Send report at 12:00 AM on the first day of every month
        crontab(hour=0, minute=0, day_of_month=1),
        # crontab(minute='*/1'),
        monthly_report.s(subject="Monthly Report"),
    )



if __name__ == "__main__":
    app.run(debug=True, threaded=True)
