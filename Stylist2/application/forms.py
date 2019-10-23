from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users, Shoppinglist
from flask_login import current_user

##This is the form for users to register with 
class RegisterForm(FlaskForm):
	first_name = StringField('First name',
		validators=[ 
		    DataRequired(),
		    Length(min=2, max=30)
	     ])
	last_name = StringField('Last name',
		validators=[
		    DataRequired(),
		    Length(min=4, max=30)
		])
	email = StringField('Email',
		validators=[
		DataRequired(),
		Email()

		])
	password = PasswordField('Password',
		validators=[
		DataRequired(),
		Length(min=6, max=15)

		])
	confirm_password = PasswordField('Confirm Password',
		validators=[
		DataRequired(),
		EqualTo('password')

		])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()  # this function queries the database to make sure the email used to 
		#sign up with is unique. 
		if user:
			raise ValidationError('Email already in use!')

##This is the form that users use to log into the web application with. 
class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[
		    DataRequired(),
		    Email()

		])
	password = PasswordField('Password',
		validators=[
		    DataRequired()

		])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	first_name = StringField('First name',
		validators=[
			DataRequired(),
			Length(min=2, max=30)
		])

	last_name = StringField('Last name',
		validators=[
		    DataRequired(),
		    Length(min=4, max=30)
		])
	email = StringField('Email',
		validators=[
		DataRequired(),
		Email()

		])
	submit =SubmitField('Update')
		
	def validate_email(self, email):
		if email.data != current_user.email:
			user = Users.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use! Please choose another')



