# wtforms
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Length, Email,EqualTo

# Register form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')


# login form
class Loginform(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


# Forgot password form
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Send Reset Link')

# Reset password form
class ResetPasswordForm(FlaskForm):
    new_password =StringField('New Password', validators=[DataRequired(),Length(min=8)])
    confirm_password= StringField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')