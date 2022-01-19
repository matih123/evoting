from wtforms.validators import DataRequired, Length, Regexp
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
	pesel = StringField('PESEL', validators=[
										    DataRequired(message="Pole wymagane."), 
										    Length(min=11, max=11, message="Błędny numer PESEL."), 
										    Regexp('^[0-9]*$', message="Błędny numer PESEL.")])
	password = PasswordField('Hasło', validators=[
                                            DataRequired(message="Pole wymagane.")])
	submit = SubmitField('Zaloguj się')