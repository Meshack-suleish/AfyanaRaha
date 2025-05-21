from flask import Flask,redirect,render_template,flash,session,request,url_for,current_app
from flask import Blueprint
from Database.models import Users,Posts,Messages,Image,ScrollingText,Orders
from extensions import bcrypt,db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required,current_user
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

update_bp = Blueprint("update",__name__,template_folder="templates")
@update_bp.before_request
def restrict_to_logged_in_users():
    if not current_user.is_authenticated:
         flash('You must be logged in to access this page.', 'warning')
         return redirect(url_for('login.login'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.Role != 'SuperAdmin':
            flash("You are not allowed to perform this action.", "danger")
            return redirect(url_for('admin.admin_dashboard',show='update'))  
        return f(*args, **kwargs)
    return decorated_function

@update_bp.route('/admin/update_user', methods=['POST','GET'])
@login_required
@admin_required
def update_user():
    user_id = request.form['user_id']
    user = Users.query.get(user_id)

    if user:
        user.username = request.form['username']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.Role = request.form['role']

        new_password = request.form['password']
        if new_password.strip():  
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        try:
           db.session.commit()
           flash('User updated successfully!', 'success')

        except:
            flash('Error while updating try again!', 'danger')

    return redirect(url_for('admin.admin_dashboard', show='update'))




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@login_required
@update_bp.route('/admin/update_post', methods=['POST'])
def update_post():
    post_id = request.form['post_id']
    post = Posts.query.get(post_id)

    if post:
        post.title = request.form['title']
        post.description = request.form['description']
        post.category = request.form['category']

        if 'image_url' in request.files:
            image = request.files['image_url']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                post.image_url = filename  

        db.session.commit()
        flash('Post updated successfully.', 'success')

    return redirect(url_for('admin.admin_dashboard', show='update'))

@login_required
@update_bp.route('/admin/delete_post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    try:
        post = Posts.query.get_or_404(post_id)
        # Set Orders.post_id = None for related orders
        orders = Orders.query.filter_by(post_id=post_id).all()
        for order in orders:
            order.post_id = None
        # Delete associated image file
        if post.image_url:
            image_path = os.path.join(current_app.static_folder, post.image_url)
            if os.path.exists(image_path):
                os.remove(image_path)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting the post: {}'.format(str(e)), 'danger')
    except Exception as e:
        flash('Unexpected error: {}'.format(str(e)), 'danger')

    return redirect(url_for('admin.admin_dashboard', show='update'))

@login_required
@update_bp.route('/admin/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)

    posts = Posts.query.filter_by(user_id=user.user_id).all()
    for post in posts:
        post.user_id = None

    db.session.delete(user)
    db.session.commit()
    flash('User deleted, and related posts updated.', 'success')

    return redirect(url_for('admin.admin_dashboard', show='update'))

@login_required
@update_bp.route('/admin/delete_message/<int:message_id>', methods=['GET'])
def delete_message(message_id):
    message = Messages.query.get_or_404(message_id)
    try:
       db.session.delete(message)
       db.session.commit()
       flash('Message deleted successfully.', 'success')
       return redirect(url_for('admin.admin_dashboard', show='messages'))
    except:
        flash('failed to delete message!','danger')
        return redirect(url_for('admin.admin_dashboard', show='messages'))
    

@update_bp.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    image_path = os.path.join(current_app.static_folder, image.filename)
    
    # Delete the file
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete from database
    try:
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard', show='settings'))

    except:
        flash('failed to delete image')
        return redirect(url_for('admin.admin_dashboard', show='settings'))


@update_bp.route('/edit_text/<int:text_id>', methods=['POST'])
@login_required
def edit_text(text_id):
    text = ScrollingText.query.get_or_404(text_id)
    new_content = request.form['content']
    try:
        text.content = new_content
        db.session.commit()
        flash("Ujumbe umehaririwa vizuri", "success")
    except:
        flash("Imeshindikana kuhariri ujumbe", "danger")
    return redirect(url_for('admin.admin_dashboard', show='settings'))

@update_bp.route('/delete_text/<int:text_id>', methods=['POST'])
@login_required
def delete_text(text_id):
    text = ScrollingText.query.get_or_404(text_id)
    try:
        db.session.delete(text)
        db.session.commit()
        flash("Ujumbe umefutwa", "success")
    except:
        flash("Kufuta ujumbe haujafanikiwa", "danger")
    return redirect(url_for('admin.admin_dashboard', show='settings'))
