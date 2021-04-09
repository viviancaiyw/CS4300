from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("blank username")])
    password = PasswordField('Password', validators=[InputRequired("blank password")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')