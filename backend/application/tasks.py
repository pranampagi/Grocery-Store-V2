from celery import shared_task
from .mail_service import send_message
from .models import User, Role, Order
from jinja2 import Template
from datetime import datetime, timedelta



# @shared_task(ignore_result=False)
# def create_product_csv():
#     prod_resource = Product.query.with_entities( Product.name, Product.price, Product.quantity, Product.sold_quantity, Product.manufacture_date).all()

#     csv_output = excel.make_response_from_query_sets(prod_resource, ["name", "price", "quantity", "sold_quantity", "manufacture_date"], "csv")
#     filename = "products.csv"

#     with open(filename, 'wb') as f:
#         f.write(csv_output.data)

#     return filename
    


@shared_task(ignore_result=True)
def daily_reminder(subject):
    users = User.query.filter(User.roles.any(Role.name == 'Customer')).all()
    for user in users:
        if user.last_login_at < datetime.now() - timedelta(days=1):
            with open('templates/reminder.html', 'r') as f:
                template = Template(f.read())
                send_message(user.email, subject, template.render(name=user.name))

    return "OK"


@shared_task(ignore_result=True)
def monthly_report(subject):
    users = User.query.filter(User.roles.any(Role.name == 'Customer')).all()

    for user in users:
        # Orders of the user in last one month
        orders = Order.query.filter(Order.user_id == user.id, Order.date >= datetime.now() - timedelta(days=30)).all()
        # Total amount of each order
        total_amount = sum([ sum([item.price * item.quantity for item in order.order_items]) for order in orders ])

        with open('templates/report.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject, template.render(orders=orders, total_amount=total_amount, name=user.name))

    return "OK"
