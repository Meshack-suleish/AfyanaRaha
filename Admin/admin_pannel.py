from flask import Blueprint,render_template,Flask,redirect,url_for,request,current_app,flash,session
from Database.models import Users,Posts,Orders,Messages,Image,ScrollingText
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from extensions import db


admin_bp = Blueprint('admin',__name__, template_folder='templates')
@admin_bp.before_request
def restrict_to_logged_in_users():
    if not current_user.is_authenticated:
         flash('You must be logged in to access this page.', 'warning')
         return redirect(url_for('login.login'))
@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_authenticated:
         flash('You must be logged in to access this page.', 'warning')
         return redirect(url_for('login.login')) 

    section = request.args.get("show")
    users = None
    posts = None
    orders = None
    if section == "update":
        users = Users.query.all()
        posts = Posts.query.all()
        return render_template("admin.html", section=section,users=users,posts=posts)
    elif section == 'orders':
        orders= db.session.query(
        Orders.order_id,
        Orders.Buyers_phone,
        Orders.Buyers_email,
        Orders.status,
        Posts.title.label('post_title')
        ).join(Posts, Orders.post_id == Posts.post_id).all()
        return render_template("admin.html", section=section,orders=orders)
    
    elif section == 'messages':
        messages = Messages.query.order_by(Messages.sent_at.desc()).all()
        return render_template("admin.html", section=section,messages=messages)
    elif section == 'users':
        return render_template("admin.html", section=section)
    elif section == 'upload':
        return render_template("admin.html", section=section)
    elif section == 'settings':
        texts = ScrollingText.query.all()
        images = Image.query.all()
        return render_template('admin.html',section=section,images=images,texts=texts)
    elif section == 'dashboard':
        new_messages = Messages.query.count()
        user_count = Users.query.count()
        post_count = Posts.query.count()
        pending_orders = Orders.query.filter_by(status='pending').count()
        return render_template('admin.html',
                           new_messages=new_messages,
                           user_count=user_count,
                           post_count=post_count,
                           pending_orders=pending_orders)
    else:
        new_messages = Messages.query.count()
        user_count = Users.query.count()
        post_count = Posts.query.count()
        pending_orders = Orders.query.filter_by(status='pending').count()
        return render_template('admin.html',
                           new_messages=new_messages,
                           user_count=user_count,
                           post_count=post_count,
                           pending_orders=pending_orders)




@admin_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user = current_user

    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    if username:
        user.username = username
    if email:
        user.email = email
    if phone:
        user.phone = phone
    if password:
        user.set_password(password)  

    db.session.commit()
    flash("Profile updated successfully", "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user() 
    session.clear()
    return redirect(url_for('login.login'))