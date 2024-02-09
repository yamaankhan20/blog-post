from flask import flash, Blueprint, redirect, url_for,  render_template, current_app
from flask_login import login_user, LoginManager, current_user
from app import bcrypt, db
from datetime import datetime

auth_controller = Blueprint('auth_controller', __name__)

login_manager = LoginManager()


@login_manager.request_loader
def load_user_from_request(request):
    return None


login_manager.init_app(auth_controller)


def login_check():
    from forms.authentication import LoginFrom
    from models.All_users import All_users
    logform = LoginFrom()
    with current_app.app_context():
        if current_user.is_authenticated:
            return redirect(url_for('user_bp.dashboard'))

        if logform.validate_on_submit():
            user = All_users.query.filter_by(email=logform.email.data).first()
            if user and bcrypt.check_password_hash(user.password, logform.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('user_bp.dashboard'))
            else:
                flash("Wrong email or password. Please try again.", 'danger')

    return render_template('login.html', form=logform)

def register_check():
    from forms.authentication import RegisterationFrom
    from models.All_users import All_users
    form = RegisterationFrom()
    if current_user.is_authenticated:
        return redirect(url_for('user_bp.dashboard'))
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data)
        new_user = All_users(name=form.name.data, email=form.email.data, password=password_hashed, date=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flash("You are registered!", "success")
        return redirect(url_for("user_bp.login"))

    return render_template('register.html', form=form)
