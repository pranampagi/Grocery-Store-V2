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


@celery_app.task(ignore_result=False)
def create_product_csv():
    prod_resource = Product.query.with_entities( Product.name, Product.price, Product.quantity, Product.sold_quantity, Product.manufacture_date).all()

    csv_output = excel.make_response_from_query_sets(prod_resource, ["name", "price", "quantity", "sold_quantity", "manufacture_date"], "csv")
    filename = "products.csv"

    with open(f"static/{filename}", 'wb') as f:
        f.write(csv_output.data)

    return filename


@app.route('/download-csv')
@auth_required("token")
@roles_accepted('Storemanager')
def download_csv():
    try:
        # time.sleep(5)
        task = create_product_csv.apply_async()
        return jsonify({"task_id": task.id}), 200
    except:
        return jsonify({"message": "Something went wrong"}), 400


@app.route('/get-csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id, backend=celery_app.backend)
    if res.ready():
        filename = res.result
        return send_file(f"static/{filename}", as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 400



if __name__ == "__main__":
    app.run(debug=True, threaded=True)
