from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet ,configure_uploads,patch_request_class
from flask_migrate import Migrate
import os 
from flask_msearch import Search
from flask_login import LoginManager

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Tarek-online.db"
app.config["SECRET_KEY"]="TarekZainAldin1990"
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/images')
photos=UploadSet('photos',IMAGES)
configure_uploads(app,photos)
patch_request_class(app)


db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
search=Search()
search.init_app(app)

login_manger=LoginManager()
login_manger.init_app(app)
login_manger.login_view='customerLogin'
login_manger.needs_refresh_message_category='danger'
login_manger.login_message=u"please login first"

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customer import routes

