######################################################################
#
#  Written by: Marvin Fuller
#  Date: Dec 26, 2015
#  Filename: mf_meals.py --
#  Purpose:
"""         The purpose of this module is an implementation of a
             dynamic webserver which will offer users a method 
             of planning Family Gathering & PotLuck type meals.
"""
#
######################################################################
# !/usr/bin/python
# -*- coding: utf-8 -*-

# Import libraries
import logging
import ConfigParser
import datetime
import operator
# Import Flask Framework Components
from flask import Flask, render_template, request, redirect, url_for,\
                  flash, jsonify, Response, make_response
from flask_stormpath import StormpathManager, login_required,\
                     groups_required, user, User,login_user, logout_user
# Import Flask-WTF and WTForms components
from webob.multidict import MultiDict
from flask_wtf import Form
from wtforms import validators, HiddenField, StringField, IntegerField
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Required, Optional, Length, NoneOf
from meals_forms import DeleteForm, SearchForm, ContributeForm, CreateForm
# Import Database ORM components
from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker
from try_db_create01 import Base, Event, Requested, Committed

# Prepare to read from meals.ini configuration file
Config = ConfigParser.ConfigParser()
# Note: This absolute location will need to be edited in production..
Config.read('/var/www/apps/Mealz/meals_conf.ini')

# Setup logging parameters
# Note: remove once deployed in production
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

app = Flask(__name__)

# Stormpath Authentication Setup  #####################################
#   Each paramter is set from the 'meals_conf.ini' config file 
app.config['SECRET_KEY'] = Config.get('SP', 'SECRET_KEY')
app.config['STORMPATH_API_KEY_FILE'] = Config.get('SP', 'API_KEY_FILE')
app.config['STORMPATH_APPLICATION'] = Config.get('SP', 'STORMPATH_APPLICATION')
# Which fields should be displayed when registering new users?
# If this is diabled, only social login can be used.
app.config['STORMPATH_ENABLE_EMAIL'] = \
           Config.getboolean('SP', 'ENABLE_EMAIL')
app.config['STORMPATH_ENABLE_USERNAME'] = \
           Config.getboolean('SP', 'ENABLE_USERNAME')
app.config['STORMPATH_ENABLE_PASSWORD'] = \
           Config.getboolean('SP', 'ENABLE_PASSWORD')
app.config['STORMPATH_ENABLE_GIVEN_NAME'] = \
           Config.getboolean('SP', 'ENABLE_GIVEN_NAME')
app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = \
           Config.getboolean('SP', 'ENABLE_MIDDLE_NAME')
app.config['STORMPATH_ENABLE_SURNAME'] = \
           Config.getboolean('SP', 'ENABLE_SURNAME')
# which fields are required for a non-social account
# (Email and password are always required, so those are not mentioned below.)
app.config['STORMPATH_REQUIRE_USERNAME'] = Config.get('SP', 'REQ_USERNAME')
app.config['STORMPATH_REQUIRE_EMAIL'] = Config.get('SP', 'REQ_EMAIL')
app.config['STORMPATH_REQUIRE_PASSWORD'] = Config.get('SP', 'REQ_PASSWORD')
app.config['STORMPATH_REQUIRE_GIVEN_NAME'] = Config.get('SP', 'REQ_GIVEN_NAME')
app.config['STORMPATH_REQUIRE_MIDDLE_NAME'] = \
           Config.getboolean('SP', 'REQ_MIDDLE_NAME')
app.config['STORMPATH_REQUIRE_SURNAME'] = Config.get('SP', 'REQ_SURNAME')
# Will new users be required to verify new accounts via email before
# they're made active?
app.config['STORMPATH_VERIFY_EMAIL'] = Config.get('SP', 'VERIFY_EMAIL')
# Configure views.  These views can be enabled or disabled.  If they're
# enabled (default), then you automatically get URL routes, working views,
# and working templates for common operations: registration, login, logout,
# forgot password, and changing user settings.
app.config['STORMPATH_ENABLE_REGISTRATION'] = \
           Config.getboolean('SP', 'ENABLE_REGISTRATION')
app.config['STORMPATH_ENABLE_LOGIN'] = \
           Config.getboolean('SP', 'ENABLE_LOGIN')
app.config['STORMPATH_ENABLE_LOGOUT'] = \
           Config.getboolean('SP', 'ENABLE_LOGOUT')
app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = \
           Config.getboolean('SP', 'ENABLE_FORGOT_PASSWORD')
app.config['STORMPATH_ENABLE_SETTINGS'] = \
           Config.getboolean('SP', 'ENABLE_SETTINGS')
# Configure URL mappings.  These URL mappings control which URLs will be
# used by Flask-Stormpath views.
app.config['STORMPATH_REGISTRATION_URL'] = Config.get('SP', 'REGISTRATION_URL')
app.config['STORMPATH_LOGIN_URL'] = Config.get('SP', 'LOGIN_URL')
app.config['STORMPATH_LOGOUT_URL'] = Config.get('SP', 'LOGOUT_URL')
app.config['STORMPATH_FORGOT_PASSWORD_URL'] = \
           Config.get('SP', 'FORGOT_PASSWORD_URL')
app.config['STORMPATH_FORGOT_PASSWORD_CHANGE_URL'] = \
           Config.get('SP', 'FORGOT_PASSWORD_CHANGE_URL')
app.config['STORMPATH_SETTINGS_URL'] = Config.get('SP', 'SETTINGS_URL')

# Configure templates.  These template settings control which templates are
# used to render the Flask-Stormpath views.
app.config['STORMPATH_BASE_TEMPLATE'] = Config.get('SP', 'BASE_TEMPLATE')
app.config['STORMPATH_REGISTRATION_TEMPLATE'] = \
           Config.get('SP', 'REGISTRATION_TEMPLATE')
app.config['STORMPATH_LOGIN_TEMPLATE'] = \
           Config.get('SP', 'LOGIN_TEMPLATE')
app.config['STORMPATH_FORGOT_PASSWORD_TEMPLATE'] = \
           Config.get('SP', 'FORGOT_PASSWORD_TEMPLATE')
app.config['STORMPATH_FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE'] = \
           Config.get('SP', 'FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE')
app.config['STORMPATH_FORGOT_PASSWORD_CHANGE_TEMPLATE'] = \
           Config.get('SP', 'FORGOT_PASSWORD_CHANGE_TEMPLATE')
app.config['STORMPATH_FORGOT_PASSWORD_COMPLETE_TEMPLATE'] = \
           Config.get('SP', 'FORGOT_PASSWORD_COMPLETE_TEMPLATE')
app.config['STORMPATH_SETTINGS_TEMPLATE'] = \
           Config.get('SP', 'SETTINGS_TEMPLATE')

# Social login configuration.
# app.config['STORMPATH_ENABLE_FACEBOOK'] = Config.get('SP', 'ENABLE_FACEBOOK')
# app.config['STORMPATH_FACEBOOK_LOGIN_URL'] = \
#           Config.get('SP', 'FACEBOOK_LOGIN_URL')
app.config['STORMPATH_ENABLE_GOOGLE'] = Config.get('SP', 'ENABLE_GOOGLE')
app.config['STORMPATH_GOOGLE_LOGIN_URL'] = Config.get('SP', 'GOOGLE_LOGIN_URL')

# After a successful login, where should users be redirected?
app.config['STORMPATH_REDIRECT_URL'] = Config.get('SP', 'REDIRECT_URL')
#app.config['STORMPATH_SOCIAL'] = Config.get('SP', 'SOCIAL')
app.config['STORMPATH_SOCIAL'] = {
    'GOOGLE': {
        'client_id': Config.get('SP', 'GOOGLE_CLIENT_ID'),
        'client_secret': Config.get('SP', 'GOOGLE_CLIENT_SECRET'),
    }
}




# Cookie configuration.
app.config['STORMPATH_COOKIE_DOMAIN'] = Config.get('SP', 'COOKIE_DOMAIN')
app.config['STORMPATH_COOKIE_DURATION'] = datetime.timedelta(minutes=30)
# Cookie name (this is not overridable by users, at least not explicitly).
app.config['REMEMBER_COOKIE_NAME'] = Config.get('SP', 'REMEMBER_COOKIE_NAME')

stormpath_manager = StormpathManager(app)

# Database Setup  ##########################################################
# Create Session and Connect to DB
# Retrieve database config info from meals.ini configuration file
engine_string = 'postgresql+psycopg2://'\
                 + Config.get('db', 'pguser') + ':'\
                 + Config.get('db', 'pguserpw') + '@'\
                 + Config.get('db', 'pghost') + '/'\
                 + Config.get('db', 'pgdatabase')
                 
# define the engine for connecting to postgres remote database
engine = create_engine(engine_string)
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.
session = DBSession()
# End Database Setup Section ################################################

# Some Global variables
categories = [ "app", "main", "side", "bread", "dessert", "bev", "uten",
               "cups", "misc"]

# Helper Functions ##########################################################
# create a function for extracting just the user ID String From Stormpath ID
def get_pure_id(input):
    '''Function takes as input the user ID String From Stormpath ID
         and extracts/returns just the pure user ID String.
    '''
    pointer = input.rindex('/') 
    output = input[(pointer +1): ]
    return output

def get_real_cat(nickname):
    '''Function takes as input the nickname of a category
         and returns the actual meal category name as a string.
    '''
    cat_list = {"app": "Appetizers", "main" : "Main Dish",
                 "side" : "Side Dish", "bread" : "Bread",
                 "dessert" : "Dessert", "bev" : "Beverages",
                 "uten" : "Utensils", "cups" : "Cups, Plates, Napkins",
                 "misc" : "Miscellaneous"}
    output = cat_list[nickname]
    return output

def check_req_db(evt_id, nickname):
    '''Function takes as input the event id & the nickname of a category
         and returns a Boolean of whether that category has been requested
         in the requested table of the db.
    '''
    try:
        cat_req = session.query(Requested).\
                  filter_by(evt_id = evt_id,\
                  category = get_real_cat(nickname)).one()
        output = True
    except:
        output = False
    return output

# #########################################################################
# Routes
# #########################################################################

# Root or Public page
@app.route('/')
@app.route('/public/')
def showPublic():
    # 3 options on this page
    # 1. Create a new event
    # 2. list my events
    # 3. Search for an event (that user has been invited to)
    #check user for authenticated and if so redirect to '/public/loggedin'
    if user.is_authenticated():
        return redirect(url_for('showLoggedin'))
    else:
        return render_template('public.html')


@app.route('/g_loggedin/')
@app.route('/public/loggedin/')
@login_required
def showLoggedin():
    # 3 options on this page
    # 1. Create a new event
    # 2. list my events
    # 3. Search for an event (that user has been invited to)
    usr_email = user.email
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_id = get_pure_id(user.get_id())
    
    print "\nCurrent user ID =" , get_pure_id(user.get_id()), user
    return render_template('loggedin.html', 
                            webemail = usr_email,
                            webfname = usr_first_name,
                            weblname = usr_last_name,
                            webusername = usr_username,
                            webuserid = usr_id)


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')

    return redirect(url_for('showPublic'))




# Create an Event Page
@app.route('/createevent/<user_id>/', methods=['GET', 'POST'])
@login_required
def create_event(user_id):
    # User should be able to create a new event & add details about event
    # Gather important details on user from Stormpath
    usr_id = get_pure_id(user.get_id())
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_email = user.email
    print "The current User is :", usr_id, "\n"

    if request.method == 'POST':
        # Gather posted data of details about this event
        form = CreateForm(formdata = MultiDict(request.form))
        if form.validate():
            # Gather details about this event
            # prepare items to be posted into event table
            date1 = datetime.date(int(form.evt_year.data),
                                  int(form.evt_month.data),
                                  int(form.evt_day.data))
            time1 = str(form.evt_hour.data + ":" +\
                        form.evt_minute.data + form.evt_tz.data)
            Event1 = Event(org_id = usr_id,
               org_username = usr_username,
               org_fname = usr_first_name,
               org_lname = usr_last_name,
               evt_num = form.evt_num.data,
               evt_date = date1,
               evt_time = time1,
               evt_name = form.evt_name.data,
               evt_location = form.evt_location.data,
               evt_address = form.evt_address.data,
               evt_city = form.evt_city.data,
               evt_state = form.evt_state.data,
               evt_zip = form.evt_zip.data,
               evt_notes = form.evt_notes.data,
               evt_image = 'party01.jpg')
            session.add(Event1)
            session.flush()
            session.refresh(Event1) # get the id of the last added event
            new_event_id = int(Event1.id)
            
            # prepare items to be posted into Requested table
            for x in categories:
                # create a reference string for current category
                field1 = "req_%s_qty" % x
                field2 = "req_%s_note" % x
                # use reference string to retrieve form data for QTY & Note 
                current_req_qty = getattr(form, field1).data
                current_req_note = getattr(form, field2).data
                # if requested QTY > 0 then persist requested data to db
                if int(current_req_qty) > 0:
                    Req1 = Requested(evt_id = new_event_id,
                             category = get_real_cat(x),
                             qty_rqst = current_req_qty,
                             rqst_note = current_req_note)
                    session.add(Req1)
                    session.flush()
           
            session.commit()
            # if data persisted correctly redirect to "List my Events"
            return redirect(url_for('list_my_events', 
                            user_id = user_id))
        else:
            # got to this point since form data was missing
            print "CreateForm did not validate!"
            flash('Enter required fields!')
            return render_template('createevent.html',
                        webform = form,
                        webevent_org_id = usr_id)
    
    else:
        # GET Method 
        return render_template('createevent.html',
                             webform = CreateForm(),
                             webevent_org_id = usr_id,
                             webuser_email = usr_email,
                             webuser_fname = usr_first_name,
                             webuser_lname = usr_last_name,
                             webuserid = usr_id)


# List MY Events Page
@app.route('/listmyevents/<user_id>/', methods=['GET', 'POST'])
@login_required
def list_my_events(user_id):
    # this page should list all of this user's events
    # Option : Open or contribute to any of the events
    # Option: Edit an event from the list
    # Option: Create a new event... redirects to '/createevent'
    # Option: Delete one of their own events... redirects to '/deleteevent'
    # Gather important details on user from Stormpath
    usr_id = get_pure_id(user.get_id())
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_email = user.email
    print "\nThe current User is :", usr_id, "\n"
    # Gather details on the user's own events
    usr_events = session.query(Event).filter_by(org_id=usr_id).all()
    # Determine the number of events originated by this user
    num_evts = len(usr_events)
    response_dict = {'0': 0}
    print "\nNumber of events for this user", num_evts
    
    # Determine the number of responses for each of these events
    for i in range(0, num_evts):
        print "\nQuery for number of committed items for this event"
        num_resp = session.query(Committed).\
                           filter_by(evt_id=(usr_events[i].id)).all()
        response_dict.update({ (usr_events[i].id) : len(num_resp) })
    
    return render_template('listmyevents.html',
                            webuserid = usr_id,
                            webfname = usr_first_name,
                            weblname = usr_last_name,
                            webusername = usr_username,
                            webevents = usr_events,
                            webrespdict = response_dict)

# Edit MY Event Page
@app.route('/editevent/<user_id>/<int:evt_id>', methods=['GET', 'POST'])
@login_required
def edit_event(user_id, evt_id):
    # User has the ability to edit an event that they created.
    # Gather important details on user from Stormpath
    usr_id = get_pure_id(user.get_id())
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_email = user.email
    print "\nThe current User is :", usr_id, "\n"
    # Gather details on this event to be edited
    print "\nQuery for Event"
    event = session.query(Event).filter_by(id=evt_id).one()
    print "\nQuery for Requested Items for this event"
    req = session.query(Requested).filter_by(evt_id=evt_id).all()
    # Initialize request qty variables Dictionary to integer
    req_qty_dct = {'req_app_qty' : 0, 'req_main_qty' : 0, 'req_side_qty' : 0,
                   'req_bread_qty' : 0, 'req_dessert_qty' : 0,
                   'req_bev_qty' : 0, 'req_uten_qty' : 0, 'req_cups_qty' : 0,
                   'req_misc_qty' :0}
    # Initialize request note variables Dictionary
    req_note_dct = {'req_app_note' : "", 'req_main_note' : "",
                    'req_side_note' : "", 'req_bread_note' : "",
                    'req_dessert_note' : "", 'req_bev_note' : "",
                    'req_uten_note' : "", 'req_cups_note' : "",
                    'req_misc_note' : ""}

    # iterate thru all categories and store requested items from db into
    #  local variable dictionaries
    for x in categories:
        # create a reference string for current category
        field1 = "req_%s_qty" % x
        field2 = "req_%s_note" % x
        # use reference string to store requested items QTY & Note
        # storing db values into dictionaries
        for item in req:
            if item.category == get_real_cat(x):
                req_qty_dct[field1] = item.qty_rqst
                req_note_dct[field2] = item.rqst_note

    # handle Posted Form Data  #########################################
    if request.method == 'POST':
        # create a dict that translates form names to database field names
        event_fields = ['evt_num', 'evt_name', 'evt_location', 'evt_address',
                        'evt_city', 'evt_state', 'evt_zip', 'evt_notes']
        # Initialize database changed trigger
        db_change = False
        # define the form, same as create event form
        form = CreateForm(formdata = MultiDict(request.form))
        # Note: I did not check for form validation in this case
        #    since form fields do not require changed data
        # ###############################################################
        # Determine which Event details need to be updated
        #   then update the database entry for Event Details that changed.
        for aa in event_fields:
            # get posted form data for current field
            form_data = getattr(form, aa).data
            # get db data for current field
            db_data = getattr(event,aa)
            if form_data != db_data:
                # db update will be required in this path
                setattr(event, aa, form_data)
                db_change = True
                session.flush()      
        # #################################################################
        # Next check for any posted changes in Date fields
        date_changed = False
        if form.evt_month.data != "--":
            date_changed = True
        if form.evt_day.data != "--":
            date_changed = True
        if form.evt_year.data != "--":
            date_changed = True
        if date_changed:
            date1 = datetime.date(int(form.evt_year.data),
                                  int(form.evt_month.data),
                                  int(form.evt_day.data))
            # persist the date change to database
            event.evt_date = date1
            db_change = True
            session.flush()
        # check for any posted changes in Time fields
        time_changed = False
        if form.evt_hour.data != "--":
            time_changed = True
        if form.evt_minute.data != "--":
            time_changed = True
        if form.evt_tz.data != "--":
            time_changed = True
        if time_changed:
            time1 = str(form.evt_hour.data + ":" +
                        form.evt_minute.data + form.evt_tz.data)
            # persist the time change to database
            event.evt_time = time1
            db_change = True
            session.flush()
        # ##################################################################
        # above are all changes to the Event table so COMMIT any changes
        if db_change:
            flash('Event Updated!')
            session.commit()
            db_change = False # reset db change trigger
        
        # ############  'REQUESTED' table updates ###########################   
        # Determine which requested amounts or notes need to be updated
        # Note: Since all the requested quantity and note fields are optional,
        #       we CANT assume that the item/category previously existed in db.
        #       So, we must first check if an item for each requested category
        #       exists in the database.  This will in turn dictate whether any 
        #       detected changes need to be Updated or Inserted. Updates and
        #       Inserts are handled differently in code.  Be AWARE. 
        #       Updated (for database items that existed in database) or 
        #       Inserted (for new form items that didnt exist in database)
        #        
        # iterate thru all categories
        for thiscat in categories:
            keyq = 'req_%s_qty' % thiscat
            keyn = 'req_%s_note' % thiscat
            form_qty = getattr(form, keyq).data
            form_note = getattr(form, keyn).data
            if form_qty or form_note:
                # form data was posted path
                if int(form_qty) == 0:
                    # POSTED form qty is 0,
                    qty_in_db = check_req_db(evt_id, thiscat)
                    if qty_in_db:
                        # in this case we want to delete the db row for this 
                        #    category in the requested table since now 0 is
                        #    requested.
                        try:
                            del_cat_req = session.query(Requested).\
                                     filter_by(evt_id = evt_id,\
                                     category = get_real_cat(thiscat)).one()
                            session.delete(del_cat_req)
                            db_change = True
                            session.flush()
                        except:
                            print "error in requested table update"    
                elif int(form_qty) > 0:
                    # POSTED form qty is > 0
                    # check does db qty exist
                    qty_in_db = check_req_db(evt_id, thiscat)
                    if qty_in_db:
                        # db qty exists, then UPDATE db qty & note
                        # check for change in form data
                        if int(form_qty) != req_qty_dct[keyq]:
                            # UPDATE db with form qty
                            qty_req = session.query(Requested).\
                                  filter_by(evt_id = evt_id,\
                                  category = get_real_cat(thiscat)).one()
                            setattr(qty_req, 'qty_rqst', form_qty)
                            db_change = True
                            session.flush()
                        if form_note != req_note_dct[keyn]:
                            # UPDATE db with form note
                            note_req = session.query(Requested).\
                                  filter_by(evt_id = evt_id,\
                                  category = get_real_cat(thiscat)).one()
                            setattr(note_req, 'rqst_note', form_note)
                            db_change = True
                            session.flush()
                    else:
                        # db qty does NOT exist, then INSERT new qty & note
                        try:
                            Req1 = Requested(evt_id = evt_id,
                                   category = get_real_cat(thiscat),
                                  qty_rqst = form_qty,
                                  rqst_note = form_note)
                            session.add(Req1)
                            db_change = True
                            session.flush()
                        except:
                            print "error: insrt new Req data not complete! "
        # all changes to Requested table are complete, so commit
        if db_change:
            flash('Event Updated!')
            session.commit()
            db_change = False # reset db_change trigger
        return redirect(url_for('list_my_events',
                        user_id = usr_id))

    else:
        # Initial GET path, no posted path
        return render_template('editevent.html',
					webform = CreateForm(),
					webuserid = usr_id,
					webuser_fname = usr_first_name,
					webuser_lname = usr_last_name,
					webuser_email =usr_email,
					webevent = event,
					webreq = req,
					web_req_app_qty = req_qty_dct['req_app_qty'],
					web_req_app_note = req_note_dct['req_app_note'],
					web_req_main_qty = req_qty_dct['req_main_qty'],
					web_req_main_note = req_note_dct['req_main_note'],
					web_req_side_qty = req_qty_dct['req_side_qty'],
					web_req_side_note = req_note_dct['req_side_note'],
					web_req_bread_qty = req_qty_dct['req_bread_qty'],
					web_req_bread_note = req_note_dct['req_bread_note'],
					web_req_dessert_qty = req_qty_dct['req_dessert_qty'],
					web_req_dessert_note = req_note_dct['req_dessert_note'],
					web_req_bev_qty = req_qty_dct['req_bev_qty'],
					web_req_bev_note = req_note_dct['req_bev_note'],
					web_req_uten_qty = req_qty_dct['req_uten_qty'],
					web_req_uten_note = req_note_dct['req_uten_note'],
					web_req_cups_qty = req_qty_dct['req_cups_qty'],
					web_req_cups_note = req_note_dct['req_cups_note'],
					web_req_misc_qty = req_qty_dct['req_misc_qty'],
					web_req_misc_note = req_note_dct['req_misc_note'],
					web_evt_id = evt_id)


# Search for an Event Page
@app.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    # User has the ability to search for an event based on Originator last name
    #  and event ID.
    # gather details about searching user
    usr_id = get_pure_id(user.get_id())
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_email = user.email
    print "The current User is :", usr_id, "\n"

    if request.method == 'POST':
        form = SearchForm(formdata = MultiDict(request.form))
        if form.validate():
            # Gather details about this event
            event = session.query(Event).filter_by(id=form.evt_id.data).one()
            flash('Event Found!')
            return redirect(url_for('contribute', 
                            org_id = event.org_id,
                            event_id = event.id))
        else:
            # got to this point since form data was missing
            flash('Enter both required fields!')
            return render_template('searchevents.html', webform = form)
    else:
        return render_template('searchevents.html', webform = SearchForm())



# Contribute to an Event Page
@app.route('/contribute/<org_id>/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def contribute(org_id, event_id):
    # user has the ability to contribute to an event
    # gather details about contributing user   
    usr_id = get_pure_id(user.get_id())
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_email = user.email
    print "The current User is :", usr_id, "\n"
    # Gather details about this event
    print "\nQuery for Event"
    event = session.query(Event).filter_by(id=event_id).one()
    # Gather details about what has been requested for this event
    print "\nQuery for Requested Items"
    req = session.query(Requested).filter_by(evt_id=event_id).all()
    # Gather details about what is committed for this event
    print "\nQuery for Committed Items"
    cmttd = session.query(Committed).filter_by(evt_id=event_id).all()

    if request.method == 'POST':
        form = ContributeForm(formdata = MultiDict(request.form))
        if form.validate():
            # Form Validated Path
            # add posted data to database at this point
            Com1 = Committed(evt_id = event_id,
                 category = form.category.data,
                 item_name = form.item.data,
                 usr_lname = usr_last_name,
                 usr_fname = usr_first_name,
                 usr_username = usr_username,
                 usr_email = usr_email,
                 usr_qty = "1",
                 usr_note = form.note.data)
            session.add(Com1)
            session.commit()
            flash('New Item committed for this event!')
            # once data is posted & persisted to database,
            #   then reload Contribute page
            return redirect(url_for('contribute', 
                            org_id = event.org_id,
                            event_id = event.id))
            
        else:
            # form did NOT validate path
            flash('Enter required fields!')
            return render_template('contribute.html',
                            webform = form,
                            webevent_org_id = event.org_id,
                            webevent_org_fname = event.org_fname,
                            webevent_org_lname = event.org_lname,          
                            webevent_name = event.evt_name,
                            webevent_date = event.evt_date,
                            webevent_time = event.evt_time,
                            webevent_location = event.evt_location,
                            webevent_address = event.evt_address,
                            webevent_city = event.evt_city,
                            webevent_state = event.evt_state,
                            webevent_zip = event.evt_zip,
                            webevent_notes = event.evt_notes,
                            webevent_image = event.evt_image,
                            webevent_id = event_id,
                            webrequested = req,
                            webcommitted = cmttd)
            
    else:
        # HTTP method is GET
        return render_template('contribute.html',
                            webform = ContributeForm(),
                            webevent_org_id = event.org_id,
                            webevent_org_fname = event.org_fname,
                            webevent_org_lname = event.org_lname,          
                            webevent_name = event.evt_name,
                            webevent_date = event.evt_date,
                            webevent_time = event.evt_time,
                            webevent_location = event.evt_location,
                            webevent_address = event.evt_address,
                            webevent_city = event.evt_city,
                            webevent_state = event.evt_state,
                            webevent_zip = event.evt_zip,
                            webevent_notes = event.evt_notes,
                            webevent_image = event.evt_image,
                            webevent_id = event_id,
                            webrequested = req,
                            webcommitted = cmttd)

# Delete an Event Page
@app.route('/delete/<org_id>/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def delete(org_id, event_id):
    # organizer has ability to delete one of their events
    # gather details about contributing user   
    usr_id = get_pure_id(user.get_id())
    usr_first_name = user.given_name
    usr_last_name = user.surname
    usr_username = user.username
    usr_email = user.email
    print "The current User is :", usr_id, "\n"
    # Gather details about this event
    print "\nQuery for Event"
    event = session.query(Event).filter_by(id=event_id).one()
    # Gather details about what has been requested for this event
    print "\nQuery for Requested Items"
    req = session.query(Requested).filter_by(evt_id=event_id).all()
    # Gather details about what is committed for this event
    print "\nQuery for Committed Items"
    cmttd = session.query(Committed).filter_by(evt_id=event_id).all()

    # verify user Id and org_id match
    if usr_id != org_id:
        flash('Event Mismatch!')
        return redirect(url_for('list_my_events',
                        user_id = usr_id))
    else:
        # user Id and org_id match
        if request.method == 'POST':
            db_change = False
            form = DeleteForm(formdata = MultiDict(request.form))
            if form.validate() and form.confirm.data:
                # Form Validated Path
                # delete this event in 3 tables
                # 1. Committed table
                for each in cmttd:
                    session.delete(each)
                db_change = True
                session.flush()
                # 2. Requested table
                for each in req:
                    session.delete(each)
                db_change = True
                session.flush()
                # 3. Event Table
                session.delete(event)
                db_change = True
                session.flush()
                if db_change:
                    flash('Event Deleted!')
                    session.commit()
                    db_change = False # reset db_change trigger
            return redirect(url_for('list_my_events',
                                       user_id = usr_id))
                        
        return render_template('deleteevent.html',
                            webform = DeleteForm(),
                            webevent_org_id = event.org_id,
                            webevent_org_fname = event.org_fname,
                            webevent_org_lname = event.org_lname,          
                            webevent_name = event.evt_name,
                            webevent_date = event.evt_date,
                            webevent_time = event.evt_time,
                            webevent_location = event.evt_location,
                            webevent_address = event.evt_address,
                            webevent_city = event.evt_city,
                            webevent_state = event.evt_state,
                            webevent_zip = event.evt_zip,
                            webevent_notes = event.evt_notes,
                            webevent_image = event.evt_image,
                            webevent_id = event_id,
                            webrequested = req,
                            webcommitted = cmttd)                


# JSON API to display event information
@app.route('/json/<int:event_id>/', methods=['GET'])
def json_evt_details(event_id):
    # This route defines a REST API for getting details about an event
    try:
        print "\nQuery for Event"
        event = session.query(Event).filter_by(id=event_id).one()
        # Gather details about what has been requested for this event
        print "\nQuery for Requested Items"
        req = session.query(Requested).filter_by(evt_id=event_id).all()
        # Gather details about what is committed for this event
        print "\nQuery for Committed Items"
        cmttd = session.query(Committed).filter_by(evt_id=event_id).all()

        # Serialize the committed items query response
        cmttds = []
        for c in cmttd:
            cmttds.append(c.serialize)

        # Serialize the committed items query response
        reqs = []
        for r in req:
            reqs.append(r.serialize)

        return jsonify(event_details = event.serialize,\
                     requested_items = reqs,\
                     committed_items = cmttds)

    except:
        response = make_response('Invalid Request', 404)
        return response
    
    


if __name__ == '__main__':
    app.secret_key = Config.get('SP', 'SECRET_KEY')
    app.csrf_enabled = True
    app.debug = Config.getboolean('flask', 'debug')
    app.run(host = '0.0.0.0', port = Config.getint('flask', 'port'))
