from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler  import APScheduler
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
scheduler = APScheduler()

def creat_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "akdsalkdlakj"
    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views 
    from .auth import auth 
    from .models import Manga,User
    create_datanase(app)

    app.register_blueprint(views,url_prefix = '/')
    return app 
    
def create_datanase(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print("Done")

def lookForManga():
    print("Test")

