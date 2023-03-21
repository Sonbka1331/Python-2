from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, Field
from wtforms.validators import InputRequired, Email, ValidationError
from typing import Optional
import shlex
import subprocess


app = Flask(__name__)


def number_length( min_value: int, max_value: int, message: Optional[str] = None):

    def _number_length(form: FlaskForm, field: Field):
        if field.data not in range(min_value, max_value):
            if message is None:
                raise ValidationError(message='Invalid input')
            raise ValidationError(message=message)
    return _number_length


class NumberValidator:

    def __init__(self, min_value: int, max_value: int, message: Optional[str] = None):
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        if field.data not in range(self.min_value, self.max_value):
            if self.message is None:
                raise ValidationError(message='Invalid input')
            raise ValidationError(message=self.message)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), number_length(min_value=1000000000, max_value=9999999999)])
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    index = IntegerField(validators=[InputRequired()])
    comment = StringField()


@app.route("/registration", methods=['POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    if form.email.errors:
        return f"Email error: {''.join(form.email.errors)}"

    return f"Invalid input, {form.errors}", 400


@app.route("/uptime")
def uptime():
    command = f"uptime --pretty"
    command = shlex.split(command)
    result_object = subprocess.run(command, capture_output=True)
    result = result_object.stdout.decode()
    return f"Current uptime: <pre>{result}</pre>"


@app.route("/ps")
def ps():
    args = request.args.getlist('arg')
    command = "ps"
    for arg in args:
        command = f"{command} {arg}"
    command = shlex.quote(command)
    result_obj = subprocess.run(command, capture_output=True)
    result = result_obj.stdout.decode()
    return f"Command \"ps\" result:<br><pre>{result}</pre>"


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
