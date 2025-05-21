from flask import Flask, redirect, render_template,request,flash,url_for
from config import Config
from extensions import db
from flask_migrate import Migrate
from Database.models import Posts,Orders,Messages,Users,Image,ScrollingText
from sqlalchemy import or_
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

from Admin.uploads.upload import upload_bp
from Admin.Login.Login import login_bp
from Admin.admin_pannel import admin_bp
from Admin.updates.update import update_bp
from Admin.orders.orders import orders_bp

from flask_login import LoginManager




app = Flask(__name__)

load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')

app.secret_key =SECRET_KEY
app.config.from_object(Config)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD  
app.config['MAIL_DEFAULT_SENDER'] = MAIL_USERNAME

mail = Mail(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER

db.init_app(app)
migrate = Migrate(app,db)
# Registered Blueprints
app.register_blueprint(upload_bp,url_prefix='/upload')
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(update_bp)
app.register_blueprint(orders_bp)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    category = request.args.get('category')
    search_query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 18 # Adjust number of posts per page

    posts_query = Posts.query

    if category:
        posts_query = posts_query.filter_by(category=category)

    if search_query:
        posts_query = posts_query.filter(Posts.description.ilike(f"%{search_query}%"))

    posts = posts_query.paginate(page=page, per_page=per_page)
    users = Users.query.filter_by(Role='SuperAdmin').first()
    images = Image.query.all()
    texts = ScrollingText.query.all()
    return render_template('index.html', posts=posts,user=users,images=images,texts=texts)



@app.route('/place-order', methods=['POST'])
def place_order():
    try:
        post_id = request.form.get('post_id')
        post_title = request.form.get('post_title')
        phone = request.form.get('phoneNumber')
        email = request.form.get('email') or None
        status = 'pending'
        # Server-side validation
        if not phone or len(phone) != 10 or not phone.isdigit():
            flash("Invalid phone number", "danger")
            return redirect(url_for('index'))  

        new_order = Orders(
            post_id=int(post_id),
            Buyers_phone=phone,
            Buyers_email=email,
            status=status
        )
        db.session.add(new_order)
        db.session.commit()
        user = Users.query.filter_by(Role='SuperAdmin').first()
        admin_email = user.email
        msg = Message("📦 New Order Received", recipients=[admin_email])
        msg.body = f"""A new order has been placed , you are receiving this email from a customer, please contact him or her:
           Post title: {post_title}
           Phone: {phone}
          Email: {email or 'N/A'}"""

        mail.send(msg)
        flash("Order yako imetumwa!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Order yako haijatumwa!, jaribu tena", "danger")

    return redirect(url_for('index'))


# Route to handle the form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message_text = request.form['message']
        senders_phone = request.form['phone']
        senders_email = request.form.get('email')  

        new_message = Messages(
            message_text=message_text,
            senders_phone=senders_phone,
            senders_email=senders_email
        )

        try:
            db.session.add(new_message)
            db.session.commit()
            flash("ujumbe wako umetumwa!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error , ujumbe haujatumwa jaribu tena", "danger")
            return redirect(url_for('index'))

    return redirect(url_for('index'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)


    