import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')  
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')      
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB', 'herbal')        
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
