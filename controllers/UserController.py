from flask import Blueprint,  render_template, request, redirect,url_for, flash
# from models import All_users, All_posts, Contact_form
from app import db
from datetime import datetime
from flask_login import current_user
import os
import random
import string


user_controller = Blueprint('user_controller', __name__)

from models.All_posts import All_posts
from models.All_users import All_users
from forms.authentication import Add_Blogs, Delete_blog, update_Blogs, Add_user_post, update_post_user_specify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def home_page():
    post_data = All_posts.query.filter_by(status= 'published').all()
    formatted_posts = []
    for post in post_data:
        formatted_date = post.date.strftime("%B %d, %Y")
        formatted_posts.append((post, formatted_date))
    return render_template('index.html', post=formatted_posts[0:])  # formatted_posts[0:2] is used for post per page

def dashboard_details():
    get_ID = current_user.id

    get_post = All_posts.query.filter_by(user_posted= get_ID).all()
    formatted_posts = []
    formatted_date= ''
    for post in get_post:
        formatted_date = post.date.strftime("%B %d, %Y")
        formatted_posts.append((post, formatted_date))

    delete_form = Delete_blog()
    if request.method == 'POST' and 'delete' in request.form:
        if delete_form.validate_on_submit():
            post_ID = request.form.get('post_id')
            if post_ID:
                delete_query = All_posts.query.get(post_ID)
                if delete_query:
                    # os.remove('static/img/' + delete_query.img_file)
                    db.session.delete(delete_query)
                    db.session.commit()
                    return redirect(url_for("user_bp.dashboard"))
                else:
                    flash("Error Accured While deleting!", "danger")
            else:
                flash("Post ID is required", "danger")

    if get_ID == 1:
        return redirect(url_for("user_bp.admin_dashboard"))

    return render_template('dashboard.html', get_post=get_post, formatted_date=formatted_date, delete_form= delete_form)

def admin_user_dashboard():
    get_ID = current_user.id
    for_date = All_posts.query.all()

    formatted_posts = []
    for post in for_date:
        formatted_date = post.date.strftime("%B %d, %Y %H:%M:%S")
        formatted_posts.append((post, formatted_date))

    if get_ID == 1:
        return render_template('admin-dashboard/admin-dashboard.html')
    else:
        return redirect(url_for('user_bp.dashboard'))

    return render_template('admin-dashboard/admin-dashboard.html', get_post = get_post, formatted_date = formatted_date)


def about_details():
    return render_template('about.html')

def post_page():
    return render_template('post.html')


def contact_page():
    from models.Contact_form import Contact_form
    if(request.method == "POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')
        all_entries = Contact_form(name=name, email=email, phone_number=phone_number, message=message, date=datetime.now())
        db.session.add(all_entries)
        db.session.commit()
    return render_template('contact.html')


def single_POST(post_slug):
    post = All_posts.query.filter_by(slug=post_slug).first()
    if not post:
        return redirect(url_for('user_bp.page_not_found'))
    formatted_date = post.date.strftime("%B %d, %Y")
    return render_template('single-post.html', post=post, formatted_date=formatted_date)




def all_blogs_details():
    for_date = All_posts.query.all()
    formatted_posts = []
    formatted_date = ""
    for post in for_date:
        formatted_date = post.date.strftime("%B %d, %Y")
        formatted_posts.append((post, formatted_date))

    delete_form = Delete_blog()
    if delete_form.validate_on_submit():
        post_ID = request.form.get('post_id')
        if post_ID:
            delete_query = All_posts.query.get(post_ID)
            if delete_query:
                # os.remove('static/img/' + delete_query.img_file)
                db.session.delete(delete_query)
                db.session.commit()
                return redirect(url_for("user_bp.all_blogs"))
            else:
                flash("Error Accured While deleting!", "danger")
        else:
            flash("Post ID is required", "danger")

    return render_template('admin-dashboard/all-blogs.html', delete_form= delete_form, for_date= for_date, formatted_posts= formatted_date)

def my_blogs_details():
    if current_user.id == 1:
        for_date = All_posts.query.filter_by(user_posted=1).all()
        formatted_posts = []
        formatted_date = ""
        for post in for_date:
            formatted_date = post.date.strftime("%B %d, %Y")
            formatted_posts.append((post, formatted_date))

        delete_form = Delete_blog()
        if delete_form.validate_on_submit():
            post_ID = request.form.get('post_id')
            if post_ID:
                delete_query = All_posts.query.get(post_ID)
                if delete_query:
                    # os.remove('static/img/' + delete_query.img_file)
                    db.session.delete(delete_query)
                    db.session.commit()
                    return redirect(url_for("user_bp.all_blogs"))
                else:
                    flash("Error Accured While deleting!", "danger")
            else:
                flash("Post ID is required", "danger")
    else:
        return redirect(url_for('user_bp.dashboard'))

    return render_template('admin-dashboard/my-blogs.html',delete_form= delete_form, for_date= for_date, formatted_posts= formatted_date)

def add_blogs_details():
    if current_user.id == 1:

        blogs_all = Add_Blogs()
        if blogs_all.validate_on_submit():
            slug_join = blogs_all.Blog_title.data
            joinedString = '-'.join(slug_join.split())

            if blogs_all.file_field.data:
                filename = secure_filename(blogs_all.file_field.data.filename)
                filename_join = ''.join(filename)
                extension = os.path.splitext(os.path.basename(filename_join))[1]
                image_code = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                new_name_file = image_code + '.' + extension
                blogs_all.file_field.data.save('static/img/' + new_name_file)
            else:
                new_name_file = 'random-image/dummy-image-square.jpg'


            new_data = All_posts(post_name=blogs_all.Blog_title.data, post_content=blogs_all.Description.data, date=datetime.now(), slug=joinedString, img_file=new_name_file , user_posted= current_user.id, status='draft')
            if new_data:
                db.session.add(new_data)
                db.session.commit()
                flash("Blog Updated!", "success")
                return redirect(url_for("user_bp.all_blogs"))
            else:
                flash("Error Accured While Posting!", "danger")
    else:
        return redirect(url_for('user_bp.dashboard'))

    return render_template('admin-dashboard/add-post.html', form_blogs = blogs_all)


def update_specific_blog(id):
    form = update_Blogs()
    post = All_posts.query.get_or_404(id)

    if current_user.id == 1:

        if request.method == 'POST' and form.validate():
            post.post_name = form.Blog_title.data
            slug_join = form.Blog_title.data
            post.slug = '-'.join(slug_join.split())
            post.post_content = form.Description.data

            if form.file_field.data:
                filename = secure_filename(form.file_field.data.filename)
                filename_join = ''.join(filename)
                extension = os.path.splitext(os.path.basename(filename_join))[1]
                image_code = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                new_name_file = image_code+'.'+extension
                form.file_field.data.save('static/img/' + new_name_file)
                post.img_file = new_name_file
            else:
                if not post.img_file:
                    filename = 'random-image/dummy-image-square.jpg'
                    post.img_file = filename


            post.status = form.status.data

            db.session.commit()
            flash("Blog Updated", "success")
            return redirect(url_for("user_bp.all_blogs"))
    else:
        return redirect(url_for('user_bp.dashboard'))

    return render_template('admin-dashboard/update-blogs.html', blogs_all=form, post=post )




# add normal post by users

def add_user_post():


    add_form_user = Add_user_post()
    if add_form_user.validate_on_submit():
        slug_join = add_form_user.Blog_title.data
        joinedString = '-'.join(slug_join.split())

        if add_form_user.file_field.data:
            filename = secure_filename(add_form_user.file_field.data.filename)
            filename_join = ''.join(filename)
            extension = os.path.splitext(os.path.basename(filename_join))[1]
            image_code = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            new_name_file = image_code + '.' + extension
            add_form_user.file_field.data.save('static/img/' + new_name_file)
        else:
            new_name_file = 'random-image/dummy-image-square.jpg'

        new_data = All_posts(post_name=add_form_user.Blog_title.data, post_content=add_form_user.Description.data,
                             date=datetime.now(), slug=joinedString, img_file=new_name_file,
                             user_posted=current_user.id, status='draft')
        if new_data:
            db.session.add(new_data)
            db.session.commit()
            flash("Blog Updated!", "success")
            return redirect(url_for("user_bp.dashboard"))
        else:
            flash("Error Accured While Posting!", "danger")
    else:
        flash('faild to submit')

    return render_template('add-post.html', form_blogs=add_form_user)

def post_edit_user(id, user_id):
    form = update_post_user_specify()
    not_found_url = ''
    user_ID = current_user.id
    # post = All_posts.query.filter_by(id= id, user_posted=user_id)
    post = All_posts.query.filter_by(id=id, user_posted=user_ID).first()

    if post:

        if request.method == 'POST':
            if form.validate():
                post.post_name = form.Blog_title.data
                slug_join = form.Blog_title.data
                post.slug = '-'.join(slug_join.split())
                post.post_content = form.Description.data

                if form.file_field.data:
                    filename = secure_filename(form.file_field.data.filename)
                    filename_join = ''.join(filename)
                    extension = os.path.splitext(os.path.basename(filename_join))[1]
                    image_code = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                    new_name_file = image_code + '.' + extension
                    form.file_field.data.save('static/img/' + new_name_file)
                    post.img_file = new_name_file
                elif not post.img_file:
                    filename = 'random-image/dummy-image-square.jpg'
                    post.img_file = filename

                db.session.commit()
                flash("Blog Updated", "success")
                return redirect(url_for("user_bp.dashboard"))
            else:
                flash(form.errors, 'danger')
    else:
        flash("No Post for this user", 'danger')
        not_found_url = True

    return render_template('update-post.html', form_blogs=form, post= post, not_found_url= not_found_url)


