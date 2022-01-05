from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email, EqualTo, Length, ValidationError
from flask_login import current_user
from bookaholic.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min =2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #wrforms validators function 
    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username already exist')
    
    def validate_email(self, email):

        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('That email already exist')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me') 
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min =2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        #check ddatabase if form input is not equalt a database,since changing
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username already exist')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()
            if email:
                raise ValidationError('That email already exist')

class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Request')

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email is None:
            raise ValidationError('No such email, Register First')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")