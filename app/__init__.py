from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'
login.session_protection = 'strong'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

from .models import User,Product,Order, Address



from app.adminstrations.forms import UserAdminView, ProductAdminView,MyAdminIndexView,HelloView
admin = Admin(app, 'Admin Panel', index_view=MyAdminIndexView())

from .models import User, Product

admin.add_view(UserAdminView(User, db.session))
admin.add_view(ProductAdminView(Product, db.session))
admin.add_view(HelloView(name='Exit'))

from app.main.views import main
from app.products.views import products
from app.orders.views import orders
from app.auth.views import auth
from app.adminstrations.views import administrations


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(orders, url_prefix='/orders')
app.register_blueprint(auth,url_prefix='/auth')
app.register_blueprint(administrations, url_prefix='/administrations')


