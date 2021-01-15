from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired


class CreateOrderForm(FlaskForm):
    colors = ['red', 'green', 'blue', 'yellow', 'black']

    count = IntegerField('Count', validators=[DataRequired()])
    color = SelectField('Color', choices=colors)
    submit = SubmitField('Done')


class UpdateOrderForm(FlaskForm):
    colors = ['red', 'green', 'blue', 'yellow', 'black']

    count = IntegerField('Count', validators=[DataRequired()])
    color = SelectField('Color', choices=colors)
    submit = SubmitField('Update')


class AddressForm(FlaskForm):
    mails = ['Нова пошта', 'Укрпошта']
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    district = StringField('Dictrict', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    mail = SelectField('Mail', choices=mails)
    number = StringField('Number', validators=[DataRequired()])

    submit = SubmitField('Done')
