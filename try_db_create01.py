######################################################################
#
#  Written by: Marvin Fuller
#  Date: Jan 23, 2016
#  Filename: try_db_create01.py --
#  Purpose:
"""         The purpose of this module is an implementation of using
             SQLAlchemy to connect to postgres database on remote server.
"""
#
######################################################################
# !/usr/bin/python
# -*- coding: utf-8 -*-

#   import libraries
import ConfigParser
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

# Test Results: This script worked to define table above, 
#                but NOTE that db had to previously exist.

# Prepare to read from meals.ini configuration file
Config = ConfigParser.ConfigParser()
# For Test Environment
#Config.read('./meals_conf.ini')
# For Production
Config.read('/var/www/apps/Mealz/meals_conf.ini')

# Establish the base for database connectivity 
Base = declarative_base()

# Define the event table in database
class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    org_id = Column(String(50), nullable=False)
    org_username = Column(String(50), nullable = False)
    org_fname = Column(String(50), nullable = False)
    org_lname = Column(String(50), nullable = False)    
    evt_num = Column(Integer, nullable = True)
    evt_date = Column(Date, nullable=False)
    evt_time = Column(String(25), nullable=False)
    evt_name = Column(String(150), nullable=False)
    evt_location = Column(String(250), nullable=False)
    evt_address = Column(String(150), nullable=False)
    evt_city = Column(String(50), nullable=False)
    evt_state = Column(String(3), nullable=False)
    evt_zip = Column(String(10), nullable=True)
    evt_notes = Column(String(250), nullable=True)
    evt_image = Column(String(128), nullable=True)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'event id' : self.id,
           'organizer id' : self.org_id,
           'organizer username' : self.org_username,
           'organizer first name' : self.org_fname,
           'organizer last name' : self.org_lname,
           'event attendee count' : self.evt_num,
           'event date' : str(self.evt_date),
           'event time' : self.evt_time,
           'event name' : self.evt_name,
           'event location' : self.evt_location,
           'event address' : self.evt_address,
           'event city' : self.evt_city,
           'event state' : self.evt_state,
           'event zipcode' : self.evt_zip,
           'event notes' : self.evt_notes,
           'event image' : self.evt_image,
        }

class Requested(Base):
    __tablename__ = 'requested'
    id = Column(Integer, primary_key=True)
    evt_id = Column(Integer, ForeignKey('event.id'))
    category = Column(String(50), nullable=False)
    qty_rqst = Column(Integer, nullable=False)
    rqst_note = Column(String(250), nullable=True)

    @property
    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'requested_note' : self.rqst_note,
            'event_id' : self.evt_id,
            'requested_category' : self.category,
            'requested quantity' : self.qty_rqst,
        }


class Committed(Base):
    __tablename__ = 'committed'
    id = Column(Integer, primary_key=True)
    evt_id = Column(Integer, ForeignKey('event.id'))
    category = Column(String(50), nullable = False)
    item_name = Column(String(50), nullable = False)
    usr_lname = Column(String(50), nullable = False)
    usr_fname = Column(String(50), nullable = False)
    usr_username = Column(String(50), nullable = False)
    usr_email = Column(String(50), nullable = False)
    usr_qty = Column(Integer, nullable = False)
    usr_note = Column(String(250), nullable = True)

    @property
    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'event id' : self.evt_id,
            'category' : self.category,
            'item name' : self.item_name,
            'user last name' : self.usr_lname,
            'user first name' : self.usr_fname,
            'username' : self.usr_username,
            'user email' : self.usr_email,
            'user quantity' : self.usr_qty,
            'user note' : self.usr_note,
        }



# Note: I had to create the db first before I could use this app to create
#       the tables inside db.

# Retrieve database config info from meals.ini configuration file
engine_string = 'postgresql+psycopg2://'\
                 + Config.get('db', 'pguser') + ':'\
                 + Config.get('db', 'pguserpw') + '@'\
                 + Config.get('db', 'pghost') + '/'\
                 + Config.get('db', 'pgdatabase')
                 
# define the engine for connecting to postgres remote database
engine = create_engine(engine_string)

# Next Line caution: only use .drop_all if you need to update db schema
#   do not leave this next line in app.  (2 hours of head banging!)
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

###################### end of database_setup
# this script worked to define table above, but NOTE that db had to 
#    previously exist.
