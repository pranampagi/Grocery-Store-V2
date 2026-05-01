from celery import shared_task
from .mail_service import send_message
from .models import User, Role, Order, Product
from jinja2 import Template
from datetime import datetime, timedelta

import pyexcel as pe

@shared_task(ignore_result=False)
def create_product_csv():
    products = Product.query.all()
    
    # Create a list of dictionaries for pyexcel
    data = []
    for product in products:
        data.append({
            "Name": product.name,
            "Price": product.price,
            "Quantity": product.quantity,
            "Sold Quantity": product.sold_quantity,
            "Manufacture Date": str(product.manufacture_date) if product.manufacture_date else ""
        })
    
    filename = "products.csv"
    filepath = f"static/{filename}"
    
    # Save using pyexcel
    pe.save_as(records=data, dest_file_name=filepath)
    
    return filename


def create_product_csv_sync():
    """Synchronous fallback for CSV export when Celery/Redis is unavailable."""
    import os
    products = Product.query.all()
    
    data = []
    for product in products:
        data.append({
            "Name": product.name,
            "Price": product.price,
            "Quantity": product.quantity,
            "Sold Quantity": product.sold_quantity,
            "Manufacture Date": str(product.manufacture_date) if product.manufacture_date else ""
        })
    
    filename = "products.csv"
    filepath = f"static/{filename}"
    
    # Ensure static directory exists
    os.makedirs("static", exist_ok=True)
    pe.save_as(records=data, dest_file_name=filepath)
    
    return filename

    


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
