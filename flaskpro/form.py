from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from wtforms import ValidationError
from flaskpro.models import User

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    

    def validate_username(self, username):       
        user = User.query.filter_by(username=username.data).first() 
        if user:
            raise ValidationError('This username already exists! Use a different username')
        
    def validate_email(self, email):             
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('Use a different Email!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    picture = FileField('Update Profile Pricture',validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



    def validate_username(self, username):       
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() 
            if user:
                raise ValidationError('This username already exists! Use a different username')
        
    def validate_email(self, email):             
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError('Use a different Email!')
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Post')

