from flask import Flask , render_template,redirect,url_for,flash,session,Blueprint
import os
from Database.models import Orders
from extensions import db
from flask_login import current_user

orders_bp = Blueprint("orders",__name__, template_folder="templates")

@orders_bp.before_request
def restrict_to_logged_in_users():
    if not current_user.is_authenticated:
         flash('You must be logged in to access this page.', 'warning')
         return redirect(url_for('login.login'))

@orders_bp.route('/delete-order/<int:order_id>', methods=['GET', 'POST'])
def delete_order(order_id):
    order = Orders.query.get_or_404(order_id)
    try:
        db.session.delete(order)
        db.session.commit()
        flash('Order deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting order: {str(e)}', 'danger')
    return redirect(url_for('admin.admin_dashboard', show='orders'))


@orders_bp.route('/verify-order/<int:order_id>', methods=['GET', 'POST'])
def verify_order(order_id):
    order = Orders.query.get_or_404(order_id)
    try:
        order.status = 'Verified'  
        db.session.commit()
        flash('Order verified successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error verifying order: {str(e)}', 'danger')
    return redirect(url_for('admin.admin_dashboard', show='orders'))
