from flask_wtf import FlaskForm

from wtforms import MultipleFileField,FileField

from wtforms import StringField, SubmitField,IntegerField,SelectField,FloatField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    categories =['Заколки','Резинки', 'Брош', 'Обруч']
    colors = ['red', 'green', 'blue', 'yellow', 'black','pink', 'white','orange']
    name = StringField('Name', validators=[DataRequired()])
    avatar = FileField('Main photo',validators=[DataRequired()])
    picture = MultipleFileField('Other photo',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price=FloatField('Price', validators=[DataRequired()])
    count=IntegerField('Count', validators=[DataRequired()])
    category = SelectField('Category', choices=categories)
    color = SelectField('Color', choices=colors)

    submit = SubmitField('Create')


class UpdateProductForm(FlaskForm):
    categories = ['Заколки', 'Резинки', 'Брош', 'Обруч']
    colors = ['red', 'green', 'blue', 'yellow', 'black','pink', 'white','orange']
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired()])
    category = SelectField('Category', choices=categories)
    color = SelectField('Color', choices=colors)
    submit = SubmitField('Update')

class EditMainPhotoForm(FlaskForm):
    avatar = FileField('Main photo', validators=[DataRequired()])
    submit = SubmitField('Update')

class EditOtherPhotoForm(FlaskForm):
    picture = MultipleFileField('Other photo', validators=[DataRequired()])
    submit = SubmitField('Update')