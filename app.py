from flask import Flask, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models.database import db

app = Flask(__name__)
# app.config.from_pyfile('config.py')

# app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tech_blogs'

# db = SQLAlchemy(app)
db.init_app(app)
app.secret_key = 'Your_secret_string'


bcrypt = Bcrypt(app)



login_manager = LoginManager()
login_manager.init_app(app)

from routes.user_bp import user_bp
app.register_blueprint(user_bp)

# from controllers.UserController import user_controller
# app.register_blueprint(user_controller)

# from forms.authentication import authentication_form
# app.register_blueprint(authentication_form)


@app.errorhandler(404)
def not_found(e):
    return redirect('/404')

from models.All_users import All_users
@login_manager.user_loader
def load_user(user_id):
    return All_users.query.get(int(user_id))



if __name__ == '__main__':

    app.run(debug=True)