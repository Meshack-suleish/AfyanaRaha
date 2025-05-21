from flask import Blueprint,render_template,Flask,redirect,url_for,request,current_app,flash,session
from extensions import db,bcrypt
from werkzeug.utils import secure_filename
from Database import models
from Database.models import Users,Image,ScrollingText
import os
from flask_login import current_user,login_required
from functools import wraps


upload_bp = Blueprint("upload",__name__,template_folder="templates")
@upload_bp.before_request
def restrict_to_logged_in_users():
    if not current_user.is_authenticated:
         flash('You must be logged in to access this page.', 'warning')
         return redirect(url_for('login.login'))
    

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.Role != 'SuperAdmin':
            flash("You are not allowed to perform this action.", "danger")
            return redirect(url_for('admin.admin_dashboard',show='users'))  
        return f(*args, **kwargs)
    return decorated_function
    

@upload_bp.route('/add_user' ,methods=['POST','GET'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        phone_number = request.form['phone']
        email = request.form['email']
        passwd = request.form['password']
        Role = 'User'
        password = bcrypt.generate_password_hash(passwd).decode('utf-8')

        new_user = models.Users(username=username, phone_number=phone_number, email=email, password=password,Role=Role)
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!', 'success')
        return redirect(url_for('upload.add_user'))

    return redirect(url_for('admin.admin_dashboard', show='users'))




# uploading a file
ALLOWED_EXTENSIONS = {'jpg','png','jpeg','gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload_item', methods=['GET', 'POST'])
@login_required
def upload_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        user_id = current_user.user_id
        category = request.form['category']

        # Validate form inputs
        if not title or not description or not user_id:
            flash("Missing required fields.")
            return redirect(url_for('admin.admin_dashboard'))

        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']

            # Ensure upload folder exists
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            image_url = os.path.relpath(file_path, start=current_app.static_folder).replace('\\', '/')

            post = models.Posts(
                user_id=user_id,
                title=title,
                description=description,
                category= category,
                image_url=image_url  
            )

            try:
                db.session.add(post)
                db.session.commit()
                flash('Post uploaded successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Upload failed, please try again.', 'danger')
                return redirect(url_for('admin.admin_dashboard',show='upload'))

            return redirect(url_for('admin.admin_dashboard', show='upload'))
        else:
            flash('Invalid file or no file selected.', 'warning')
            return redirect(url_for('admin.admin_dashboard', show='upload'))
        
    return render_template('upload.html')

@upload_bp.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                new_image = Image(filename=f'uploads/{filename}')
                db.session.add(new_image)
                db.session.commit()
                flash('image uploaded successfuly!','success')
                return redirect(url_for('admin.admin_dashboard', show='settings'))
            except:
                flash('failed to upload !','danger')
                return redirect(url_for('admin.admin_dashboard', show='settings'))


    return render_template('settings.html')


@upload_bp.route('/upload_text',methods=['POST','GET'])
@login_required
def upload_text():
     if request.method == 'POST':
        content = request.form['content']
        new_text = ScrollingText(content=content)
        try:
          db.session.add(new_text)
          db.session.commit()
          flash("text uploaded succesfully",'success')
          return redirect(url_for('admin.admin_dashboard', show='settings'))
        except:
            flash('failed to upload !','danger')
            return redirect(url_for('admin.admin_dashboard', show='settings'))

     return render_template('settings.html')
