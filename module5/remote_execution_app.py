from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange
import subprocess

app = Flask(__name__)


class ExecForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(0, 30)])


@app.route("/remote_execution", methods=['POST'])
def remote_exec():
    form = ExecForm()

    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        if 'shell=True' in code:
            return f"Not allowed to use 'shell=True'", 400
        code = f'prlimit --nproc=1:1 python3 -c "{code}"'
        proc = subprocess.Popen(code, stdout=subprocess.PIPE, shell=True)
        try:
            outs, errs = proc.communicate(timeout=timeout)
            # return errs
            # if errs != '':
            #     return f"You have an error in code: {errs}", 400
            return f"Execution success.<br>{outs}"
        except subprocess.TimeoutExpired:
            proc.kill()
            return f"Execution failed.<br>Timeout ends."

    return f"Invalid input, {form.errors}", 400


if __name__ == '__main__':
    app.run(debug=True)