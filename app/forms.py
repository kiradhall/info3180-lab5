from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = StringField('Description', widget=TextArea(), validators=[InputRequired()])
    poster = FileField('Poster', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])