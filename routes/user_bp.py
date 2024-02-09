from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from functools import wraps

user_bp = Blueprint('user_bp', __name__)

from controllers.UserController import home_page, dashboard_details, about_details, post_page, contact_page, single_POST, admin_user_dashboard, all_blogs_details, add_blogs_details, my_blogs_details, update_specific_blog
from controllers.auth_controller import login_check, register_check



@user_bp.route('/')
def home():
    return home_page()


@user_bp.route('/login', methods=["GET", "POST"])
def login():
    validate_data = login_check()
    if not validate_data:
        flash("User Doesn't Exists!!")
    return validate_data


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.home'))

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    validate_data = register_check()
    return validate_data


@user_bp.route('/dashboard')
@login_required
def dashboard():
    dashboard  = dashboard_details()
    return dashboard


# NORMAL PAGES ROUTE STARTS HERE

@user_bp.route('/about')
def about():
    return about_details()

@user_bp.route('/post')
def posts():
    return post_page()


@user_bp.route('/contact-us' , methods=["GET","POST"])
def contact_us():
    return contact_page()


@user_bp.route('/post/<string:post_slug>', methods=["GET","POST"])
def sinlge_post(post_slug):
    return single_POST(post_slug)

@user_bp.route('/404')
def page_not_found():
    return render_template('404.html'), 404

@user_bp.route('/admin-dashboard')
@login_required
def admin_dashboard():
    return admin_user_dashboard()

@user_bp.route('/all-blogs' , methods=["GET","POST"])
def all_blogs():
    return all_blogs_details()

@user_bp.route('/add-blogs', methods=["GET","POST"])
def add_blogs():
    return add_blogs_details()

@user_bp.route('/my-blogs', methods=["GET","POST"])
def my_blogs():
    return my_blogs_details()


@user_bp.route('/update-blog/<int:id>', methods=["GET","POST"])
def update_blog(id):
    return update_specific_blog(id)