from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    status = SelectField("Status", choices=[("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")], default="todo")
    priority = SelectField("Priority", choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("urgent", "Urgent")], default="medium")
    due_date = StringField("Due Date (YYYY-MM-DD)", validators=[Optional()])
    submit = SubmitField("Save")
