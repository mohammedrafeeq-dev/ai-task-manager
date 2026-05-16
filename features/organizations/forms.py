from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class OrganizationForm(FlaskForm):
    name = StringField("Organization Name", validators=[DataRequired(), Length(max=255)])
    slug = StringField("URL Slug", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Create Organization")
