from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class ExperimenterForm(FlaskForm):
    parameter = RadioField('parameter', choices = [("open questions","open questions"),
     ("closed questions","closed questions"), ("yes/no","yes/no")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class ContentionForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    despositions = {}
    despositions["climate"] = RadioField('Do you think drastic actions are necessary for climate change', choices = [("yes",1),
     ("no",-1)])
    

    