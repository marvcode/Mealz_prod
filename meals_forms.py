######################################################################
#
#  Written by: Marvin Fuller
#  Date: Started:Dec 26, 2015, Finished July 2016
#  Filename: meals_forms.py
#  Purpose:
"""         This module provides arll the necessary forms for the 
             implementation of a dynamic webserver which will offer users 
             a method of planning Family Gathering & PotLuck type meals.
"""
#
######################################################################

# Import Flask-WTF and WTForms components
from webob.multidict import MultiDict
from flask_wtf import Form
from wtforms import validators, HiddenField, StringField, IntegerField
from wtforms import SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Required, Optional, Length, NoneOf

# Form Classes  #######################################################
class CreateForm(Form):
    evt_num = IntegerField("Expected number of Attendees:",
                    validators=[Optional()],
                    description="best guess at number of people to attend")
    evt_name = StringField("Event Name:", validators=[
                  DataRequired(message="Please enter Event Name!")],
                  description = "like... Bob's Retirement, or Zoe's Birthday")
    evt_location = StringField(" Event Location:", validators=[
                  DataRequired(message="Please enter Event Location")],
                  description = "like... our house or Community Center")
    evt_address = StringField(" Event Address:", validators=[
                  DataRequired(message="Please enter Event Address")],
                  description = "street address")
    evt_city = StringField(" Event City:", validators=[
                  DataRequired(message="Please enter Event City")],
                  description = "city")
    evt_state = StringField("Event State:", validators=[
                  DataRequired(message="Please enter Event State")],
                  description = "")
    evt_zip = StringField("Event Zip:", validators=[
                  Optional()],
                  description = "")
    evt_notes = StringField("Notes about Event:", validators=[
                  Optional()],
                  description = "any notes that you want attendees to see...")
    evt_month = SelectField("Date", default= "--",
                   choices=[("--" , "--"),
                            ("1" , "January"),
                            ("2" , "February"),
                            ("3" , "March"),
                            ("4" , "April"),
                            ("5" , "May"),
                            ("6" , "June"),
                            ("7" , "July"),
                            ("8" , "August"),
                            ("9" , "September"),
                            ("10" , "October"),
                            ("11" , "November"),
                            ("12" , "December")], 
                  validators=[
                  NoneOf("--", message="Choose a Month")])
    evt_day = SelectField("Day", default= "--",
                   choices=[("--" , "--"),
                            ("1" , "1"),
                            ("2" , "2"),
                            ("3" , "3"),
                            ("4" , "4"),
                            ("5" , "5"),
                            ("6" , "6"),
                            ("7" , "7"),
                            ("8" , "8"),
                            ("9" , "9"),
                            ("10" , "10"),
                            ("11" , "11"),
                            ("12" , "12"),
                            ("13" , "13"),
                            ("14" , "14"),
                            ("15" , "15"),
                            ("16" , "16"),
                            ("17" , "17"),
                            ("18" , "18"),
                            ("19" , "19"),
                            ("20" , "20"),
                            ("21" , "21"),
                            ("22" , "22"),
                            ("23" , "23"),
                            ("24" , "24"),
                            ("25" , "25"),
                            ("26" , "26"),
                            ("27" , "27"),
                            ("28" , "28"),
                            ("29" , "29"),
                            ("30" , "30"),
                            ("31" , "31")], 
                  validators=[
                  NoneOf("--", message="Choose a day")])
    evt_year = SelectField("Year", default= "--",
                   choices=[("--" , "--"),
                            ("2016" , "2016"),
                            ("2017" , "2017"),
                            ("2018" , "2018")], 
                  validators=[
                  NoneOf("--", message="Choose a year")])
    evt_hour = SelectField("Hour", default= "--",
                   choices=[("--" , "--"),
                            ("1" , "1"),
                            ("2" , "2"),
                            ("3" , "3"),
                            ("4" , "4"),
                            ("5" , "5"),
                            ("6" , "6"),
                            ("7" , "7"),
                            ("8" , "8"),
                            ("9" , "9"),
                            ("10" , "10"),
                            ("11" , "11"),
                            ("12" , "12")],
                   validators=[
                   NoneOf("--", message = "Choose a Time")])
    evt_minute = SelectField("Minute", default = "--",
                   choices=[("--" , "--"),
                            ("00" , "00"),
                            ("15" , "15"),
                            ("30" , "30"),
                            ("45" , "45")],
                   validators = [
                   NoneOf("--", message = "Choose a Time")])
    evt_tz = SelectField("Timezone", default= "--",
                   choices=[("--" , "--"),
                            ("am" , "am"),
                            ("pm" , "pm")],
                   validators=[
                   NoneOf("--", message="Choose a Time")])
    req_app_qty = StringField("Appetizers", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Appetizer Quantity Needed")
    req_app_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_main_qty = StringField("Main Dish", default = 0,
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Main Dish Quantity Needed")
    req_main_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_side_qty = StringField("Side Dish", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Side Dish Quantity Needed")
    req_side_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_bread_qty = StringField("Bread", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Bread Quantity Needed")
    req_bread_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_dessert_qty = StringField("Dessert", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Dessert Quantity Needed")
    req_dessert_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_bev_qty = StringField("Beverages", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Beverage Quantity Needed")
    req_bev_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_uten_qty = StringField("Utensils", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Utensil Quantity Needed")
    req_uten_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_cups_qty = StringField("Cups, Plates, Napkins", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Cups, Plates, Napkins Quantity Needed")
    req_cups_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")
    req_misc_qty = StringField("Miscellaneous", default = "0",
                   validators = [
                   DataRequired(message = "Please enter data")],
                   description = "Enter Misc. Quantity Needed")
    req_misc_note = StringField("Note",
                   validators = [
                   Optional()],
                   description = "enter any notes about this category...")

class DeleteForm(Form):
    confirm = BooleanField("I understand that I can't undo\
                          the deletion of this event",\
                [validators.DataRequired(message='Please confirm deleteion')])

class SearchForm(Form):
    org_lname = StringField("Originator's Last Name",
                   [validators.DataRequired(message='Please enter last name')])
    evt_id = StringField("Event ID",
                   [validators.DataRequired()])

class ContributeForm(Form):
    category = SelectField(u"Categories", default= "--",
                   choices=[("--" , "--"),
                            ("Appetizers" , "Appetizers"),
                            ("Main Dish" , "Main Dish"),
                            ("Side Dish" , "Side Dish"),
                            ("Bread" , "Bread"),
                            ("Dessert" , "Dessert"),
                            ("Beverages" , "Beverages"),
                            ("Utensils" , "Utensils"),
                            ("Cups, Plates, Napkins" , "Cups, Plates, Napkins"),
                            ("Miscellaneous" , "Miscellaneous")], 
                  validators=[
                  NoneOf("--", message="Choose a Category!")])
    item = StringField("Dish Name", validators=[
                  DataRequired(message="pah-lease give me some data!")],
                  description = "add name of dish")
    note = StringField("Note", validators=[
                  Optional()],
                  description="notes on this item")

