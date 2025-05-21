from extensions import db
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
from sqlalchemy.sql import func
from sqlalchemy import DateTime,Column,text
from flask_login import UserMixin




class Users(UserMixin,db.Model):
    user_id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(10),nullable=False)
    password = db.Column(db.String(100))
    Role = db.Column(db.String(100),nullable=True)

    def get_id(self):
        return str(self.user_id)
    
    def check_password(self, passwd):
        return bcrypt.check_password_hash(self.password, passwd)


class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.user_id, ondelete='CASCADE'),nullable=False)
    title = db.Column(db.String(100), nullable = False )
    description = db.Column(db.Text,nullable =False)
    image_url = db.Column(db.String(100))
    category = db.Column(db.String(100))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)



class Orders(db.Model):
    order_id = db.Column(db.Integer,primary_key = True)
    post_id = db.Column(db.Integer,db.ForeignKey(Posts.post_id, ondelete='CASCADE'),nullable=True)
    Buyers_phone = db.Column(db.String(10),nullable = False)
    Buyers_email =db.Column(db.String(100), nullable =True)
    status = db.Column(db.String(100), default='Pending')


class Messages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.Text,nullable=False)
    sent_at = db.Column(db.DateTime,server_default=text('CURRENT_TIMESTAMP'), nullable=False )
    senders_phone = db.Column(db.String(10),nullable = False)
    senders_email = db.Column(db.String(100),nullable=True)


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Image {self.filename}>"    
    
    
class ScrollingText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScrollingText id={self.id} content='{self.content}'>"