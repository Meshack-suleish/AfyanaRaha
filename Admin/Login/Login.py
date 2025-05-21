from flask import Blueprint,redirect,render_template,url_for,session,request,flash
from Database.models import Users
from flask_login import login_user

login_bp = Blueprint("login",__name__,template_folder="templates")

@login_bp.route("/log")
def index():
    return render_template('Login.html')

@login_bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username = username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.admin_dashboard'))
        else:
          flash('Invalid credentials, try again','danger')
          return render_template('Login.html')
    return render_template('Login.html')
    