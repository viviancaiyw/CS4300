from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired, ValidationError
import re
import json
from app.utilities.import_datasets import game_genres



class search_form(FlaskForm):
    players = RadioField(label='PLAYERS', choices=[('single-player','single'), ('multi-player','multi'), ('both','both')], validators=[InputRequired("Please select your preferred game mode")])
    genres = StringField('GENRE')
    movie = StringField('Movie', validators=[DataRequired("Please enter your preferred movie")])
    tags = StringField('TAGS')
    submit = SubmitField('Submit')

    def validate_tags(self, tags):
        if tags.data:
            pattern = re.compile(r'[^\w\s]+')
            lst = []
            data = json.loads(tags.data)
            for entry in data:
                lst.append(entry['value'])
            for entry in lst:
                if re.findall(pattern, entry):
                    raise ValidationError("Illegal Character Detected! Please enter up to five words separated by space")
            if len(lst) > 5:
                raise ValidationError("Maximum Words Exceeded! Please enter up to five words separated by space")
