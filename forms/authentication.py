from flask import flash, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators, BooleanField, TextAreaField, HiddenField,  SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired, EqualTo
from models.All_users import All_users

# authentication_form = Blueprint('authentication_form', __name__)


class RegisterationFrom(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=40)], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), InputRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField("password",validators=[InputRequired(), EqualTo('confirm_password', message='Passwords Must Match!'), Length(min=5, max=225)], render_kw={"class": "form-control"})
    confirm_password = PasswordField("Comfirm Password",validators=[InputRequired() ,Length(min=5, max=225)], render_kw={"class": "form-control"})
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary btn-lg"})

    def validate_email(self, email):
        existing_email = All_users.query.filter_by(email=email.data).first()
        if existing_email:
            flash('Email already registered')
            raise ValidationError('Email already registered')

class LoginFrom(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min= 1, max=40)], render_kw = {"class":"form-control mb-3", "placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min= 5, max=225)], render_kw = {"class":"form-control", "placeholder":"Password"})
    submit = SubmitField("Login", render_kw = {"class":"btn btn-primary btn-lg"})




class Add_Blogs(FlaskForm):
    Blog_title = StringField(validators=[InputRequired(), Length(min=1, max=40)], render_kw={"placeholder": "Type here", "class": "form-control"})
    Description = TextAreaField('Description', validators=[InputRequired()], render_kw={"placeholder": "Type here", "class": "form-control"})
    submit = SubmitField("Publish", render_kw={"class": "btn btn-md rounded font-sm hover-up"})



class Delete_blog(FlaskForm):
    delete = SubmitField("Delete", render_kw={"class": "btn btn-sm font-sm btn-light rounded"})

class update_Blogs(FlaskForm):
    Blog_title = StringField('Title', validators=[InputRequired(), Length(min=1, max=40)],
                             render_kw={"placeholder": "Type here", "class": "form-control"})
    Description = TextAreaField('Description', validators=[InputRequired()],
                                render_kw={"placeholder": "Type here", "class": "form-control"})
    status = SelectField('Status', choices=[('draft', 'Draft'), ('published', 'Published')],
                         render_kw={"class": "form-select"})
    submit = SubmitField("Publish", render_kw={"class": "btn btn-md rounded font-sm hover-up"})