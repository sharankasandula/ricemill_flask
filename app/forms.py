import re

from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, FloatField, StringField,
                     PasswordField, SubmitField, DateField, SelectField,
                     TextAreaField, RadioField)
from wtforms.validators import (DataRequired, InputRequired,
                                ValidationError, EqualTo, Email, Optional)

from app import app
from app.models import User, Roles, Variety, SaleAgent, PurchaseAgent
from app import utilities


def validate_number(mobile):
    rule = re.compile(r'^(?:\+?44)?[07]\d{9,13}$')
    return rule.search(mobile)


class ChoiceValidator(object):
    def __init__(self, choice=None):
        if not choice:
            choice = "choice"
        self.message = f"Please select a valid {choice}"

    def __call__(self, form, field):
        print(f"Choice: {field.data}, {type(field.data)}")

        if field.data == 0:
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="UserName is required"),
        InputRequired(message="UserName is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="UserName is required"),
        InputRequired(message="UserName is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    email = StringField('Email', validators=[Email()])
    roles = SelectField('Role', coerce=int, validators=[
        DataRequired(message="Role is required"),
        InputRequired(message="Role is required")],
        choices=utilities.getRoles()
    )
    submit = SubmitField('Add User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AgentForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Name is required"),
        InputRequired(message="Name is required")]
    )
    email = StringField("E-Mail")
    mobile = StringField("Mobile Phone", validators=[
        DataRequired(message="Phone Number is required"),
        InputRequired(message="Phone Number is required")]
    )
    address = TextAreaField("Address", validators=[
        DataRequired(message="Address is required"),
        InputRequired(message="Address is required")
    ])
    agent_type = SelectField("Agent", validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required"),
        ChoiceValidator(choice="Agent")],
        choices=[("", "Select"), ("1", "Purchase"), ("2", "Sales")]
    )
    submit = SubmitField('Add Agent')

    def validate(self):
        agent_model = PurchaseAgent if self.agent_type.data == '1' else SaleAgent
        app.logger.info(str(self.agent_type.data) + str(self.name.data))
        user = agent_model().query.filter_by(name=self.name.data, mobile=self.mobile.data).first()
        if user is not None:
            app.logger.info(user)
            raise ValidationError('Please use a different agent name and mobile number')
        return True

    def validate_mobile(self, mobile):
        if not validate_number(mobile.data):
            raise ValidationError('Invalid mobile number')


class VarietyForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Variety Name is required"),
        InputRequired(message="Variety Name is required")]
    )
    submit = SubmitField('Add Variety')

    def validate_name(self, name):
        variety = Variety.query.filter_by(name=name.data).first()
        if variety is not None:
            raise ValidationError('Please use a different name for variety.')


class PurchaseForm(FlaskForm):
    rst_number = FloatField('RST No', validators=[
        DataRequired(message="RST Number is required"),
        InputRequired(message="RST Number is required")
    ])
    weight = FloatField("Weight", validators=[
        DataRequired(message="Weight is required"),
        InputRequired(message="Weight is required")
    ])
    variety = SelectField("Variety", coerce=int, validators=[
        DataRequired(message="Variety is required"),
        InputRequired(message="Variety is required"),
        ChoiceValidator(choice="Variety")]
    )
    agent = SelectField("Agent", coerce=int, validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required"),
        ChoiceValidator(choice="Agent")]
    )
    moisture = FloatField("Moisture", validators=[
        DataRequired(message="Moisture is required"),
        InputRequired(message="Moisture is required")
    ])
    rate = FloatField("Rate", validators=[
        DataRequired(message="Rate is required"),
        InputRequired(message="Rate is required")
    ])
    date = DateField("Date", format="%d-%m-%Y")
    amount = FloatField("Amount", validators=[
        DataRequired(message="Amount is required"),
        InputRequired(message="Amount is required")
    ])
    submit = SubmitField('Submit')


class SalesForm(FlaskForm):
    party_name = StringField("PartyName", validators=[
        DataRequired(message="PartyName is required"),
        InputRequired(message="PartyName is required")]
    )
    party_address = TextAreaField("PartyAddress", validators=[
        DataRequired(message="PartyAddress is required"),
        InputRequired(message="PartyAddress is required")
    ])
    gst_number = StringField("GST Number", validators=[
        DataRequired(message="GST Number is required"),
        InputRequired(message="GST Number is required")]
    )
    vehicle_number = StringField("Vehicle Number", validators=[
        DataRequired(message="Vehicle Number is required"),
        InputRequired(message="Vehicle Number is required")]
    )
    no_of_bags = IntegerField("Number of Bags", validators=[
        DataRequired(message="Number of Bags is required"),
        InputRequired(message="Number of Bags is required")
    ])
    variety = SelectField("Variety", coerce=int, validators=[
        DataRequired(message="Variety is required"),
        InputRequired(message="Variety is required")]
    )
    agent = SelectField("Agent", coerce=int, validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required")]
    )
    quintol = FloatField("Quintol", validators=[
        DataRequired(message="Quintol is required"),
        InputRequired(message="Quintol is required")
    ])
    rate = FloatField("Rate", validators=[
        DataRequired(message="Rate is required"),
        InputRequired(message="Rate is required")
    ])
    date = DateField("Date", format="%d-%m-%Y")
    amount = FloatField("Amount", validators=[
        DataRequired(message="Amount is required"),
        InputRequired(message="Amount is required")
    ])
    submit = SubmitField('Submit')
