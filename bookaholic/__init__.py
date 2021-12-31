from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8bf452767368d7eb212c70163649465a'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# decorater login_required, where the login route is located
login_manager.login_view = 'login'
#decorater how the error should be displayed 
login_manager.login_message_category = 'info' 
#after logged in directly to the page we were trying to access rather than home page



from bookaholic import routes