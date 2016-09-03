######################################################################
#
#  Written by: Marvin Fuller
#  Date: Dec 26, 2015
#  Filename: example_ini_set.py --
#  Purpose:
"""         The purpose of this module is to show an example of 
             how to set some config variables needed for the 'Mealz' project.
             I have stripped all my persoanl info out and you will need to put 
             your correct info in.  Examples are user name and passwords.
"""
#
######################################################################
# !/usr/bin/python
# -*- coding: utf-8 -*-

# Import libraries
import ConfigParser
from datetime import timedelta

Config = ConfigParser.ConfigParser()

# Create the config file
cfgfile = open("./meals_conf.ini",'w')

# add the settings to the structure of the file, and lets write it out...
# Stormpath Section
Config.add_section('flask')
Config.set('flask', 'debug', True) # Change to False before Deploying
Config.set('flask', 'port', 5000)

Config.add_section('SP')
Config.set('SP', 'API_KEY_FILE', '/home/vagrant/.stormpath/apiKey.properties')
Config.set('SP', 'SECRET_KEY', 'your_own_secret')
Config.set('SP', 'STORMPATH_APPLICATION', 'Meals')
# Which fields should be displayed when registering new users?
Config.set('SP', 'ENABLE_FACEBOOK', False)
Config.set('SP', 'ENABLE_GOOGLE', True)
# If ENABLE_EMAIL is diabled, only social login can be used.
Config.set('SP', 'ENABLE_EMAIL', True)  
Config.set('SP', 'ENABLE_USERNAME', True)
Config.set('SP', 'ENABLE_EMAIL', True)     # This MUST be True!
Config.set('SP', 'ENABLE_PASSWORD', True)  # This MUST be True!
Config.set('SP', 'ENABLE_GIVEN_NAME', True)
Config.set('SP', 'ENABLE_MIDDLE_NAME', False)
Config.set('SP', 'ENABLE_SURNAME', True)
# If the user attempts to create a non-social account, which fields should
# we require?  (Email and password are always required, so those are not
# mentioned below.)
Config.set('SP', 'REQ_USERNAME', True)
Config.set('SP', 'REQ_EMAIL', True)    # This MUST be True!
Config.set('SP', 'REQ_PASSWORD', True) # This MUST be True!
Config.set('SP', 'REQ_GIVEN_NAME', True)
Config.set('SP', 'REQ_MIDDLE_NAME', False)
Config.set('SP', 'REQ_SURNAME', True)
# Will new users be required to verify new accounts via email before
# they're made active?
Config.set('SP', 'VERIFY_EMAIL', True)
# Configure views.  These views can be enabled or disabled.  If they're
# enabled (default), then you automatically get URL routes, working views,
# and working templates for common operations: registration, login, logout,
# forgot password, and changing user settings.
Config.set('SP', 'ENABLE_REGISTRATION', True)
Config.set('SP', 'ENABLE_LOGIN', True)
Config.set('SP', 'ENABLE_LOGOUT', True)
Config.set('SP', 'ENABLE_FORGOT_PASSWORD', True)
Config.set('SP', 'ENABLE_SETTINGS', True)
# Configure URL mappings.  These URL mappings control which URLs will be
# used by Flask-Stormpath views.
Config.set('SP', 'REGISTRATION_URL', '/register')
Config.set('SP', 'LOGIN_URL', '/login')
Config.set('SP', 'LOGOUT_URL', '/logout')
Config.set('SP', 'FORGOT_PASSWORD_URL', '/forgot')
Config.set('SP', 'FORGOT_PASSWORD_CHANGE_URL', '/forgot/change')
Config.set('SP', 'SETTINGS_URL', '/settings')
# original
# Config.set('SP', 'GOOGLE_LOGIN_URL', '/public/loggedin')
#change in debug effort
Config.set('SP', 'GOOGLE_LOGIN_URL', '/g_loggedin/')
Config.set('SP', 'FACEBOOK_LOGIN_URL', '/facebook')
Config.set('SP', 'GOOGLE_CLIENT_ID', '...your google client ID')
Config.set('SP', 'GOOGLE_CLIENT_SECRET', '...your google client secret')

# After a successful login, where should users be redirected?
Config.set('SP', 'REDIRECT_URL', '/public/loggedin/')
# Cache configuration.
# Config.set('SP', 'CACHE', None)
# Configure templates.  These template settings control which templates are
# used to render the Flask-Stormpath views.
Config.set('SP', 'BASE_TEMPLATE', 'flask_stormpath/base.html')
Config.set('SP', 'REGISTRATION_TEMPLATE', 'flask_stormpath/register.html')
Config.set('SP', 'LOGIN_TEMPLATE', 'flask_stormpath/login.html')
Config.set('SP', 'FORGOT_PASSWORD_TEMPLATE', 'flask_stormpath/forgot.html')
Config.set('SP', 'FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE',
                 'flask_stormpath/forgot_email_sent.html')
Config.set('SP', 'FORGOT_PASSWORD_CHANGE_TEMPLATE', 
                 'flask_stormpath/forgot_change.html')
Config.set('SP', 'FORGOT_PASSWORD_COMPLETE_TEMPLATE', 
                 'flask_stormpath/forgot_complete.html')
Config.set('SP', 'SETTINGS_TEMPLATE', 'flask_stormpath/settings.html')
# Social login configuration.
#Config.set('SP', 'SOCIAL', {})
Config.set('SP', 'SOCIAL', {
    'GOOGLE': {
        'client_id' : '...your google client ID',
        'client_secret' : '...your google client secret'
    }})

# Cookie configuration.
#Config.set('SP', 'COOKIE_DOMAIN', 'dev.localhost:5000')
Config.set('SP', 'COOKIE_DOMAIN', '127.0.0.1:5000')
Config.set('SP', 'COOKIE_DURATION', timedelta(minutes=30))
# Cookie name (this is not overridable by users, at least not explicitly).
Config.set('SP', 'REMEMBER_COOKIE_NAME', 'stormpath_token')


Config.add_section('db')
Config.set('db', 'pgdatabase', 'mftrymeals')  # Change this to your values
Config.set('db', 'pghost', '10.0.1.38')  # Change this to your values
Config.set('db', 'pguser', 'sid')   # Change this to your userid
Config.set('db', 'pguserpw', 'foo.bar') # Change this to your password
# example ('postgresql+psycopg2://sid:foo.bar@10.0.1.38/mftrymeals')

# write all contents to config file & close file
Config.write(cfgfile)
cfgfile.close()

# Verification read of the new file
Config.read('./meals_conf.ini')
if Config.has_section('SP'):
    print ">>>>>  Configuration setings stored properly  <<<<<<<"



cfgfile.close()