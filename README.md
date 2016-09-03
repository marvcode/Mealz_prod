<center> Project: Item Catalog </center>
==
<center> Application Name: Mealz </center>
==
--

For my <B>Item Catalog</B> project, I chose to create a meal planning application for family gatherings and potluck dinners.

<B>EXPLANATION:</B>  This project was used for as a project for my Udacity Full Stack Web Developer Nano-degree. Essentially, this is just a learning project that uses python code to interact with the Postgres database.

####What is Mealz??####
Mealz is _potluck_ or _family gathering_ planner that will help you organize your next event.

Mealz is web app that allows an event organizer to:
+ Create an event - with all details
+ Frame the Menu - up to 9 categories of items to bring
+ Invite & Allow others to contribute some items to the event

Features:
+ Easy to understand web interface  
+ CRUD functions for each created event  
+ Secure 3rd party Authentication & Authorization  
+ CSRF protection thru 3rd party authentication token  
+ Social Media Account login  
+ json API  


# Quick Start (How to run the application):#
First things First... To run the python application several prerequisites will be required :

###Prerequisites:###

>1. Install Frameworks and libraries
2. Create a Mealz Configuration File
3. Create an SQL Database (I usedPostgres 9.4)
4. Create a Stormpath Account
5. Create a Google Developer Account


###Install these libraries on your computer:#

    sudo pip install webob
    sudo pip install flask_wtf
    sudo pip install wtforms
    sudo pip install ConfigParser
    sudo pip install flask
    sudo pip install flask.ext.stormpath
    sudo pip install psycopg2  

  
###Mealz Configuration File:#
A key element of this app is managing all the configuration parameters.  I utilized a library called ConfigParser.  <https://docs.python.org/2/library/configparser.html>

I used ConfigParser to create a configuration file called

    meals_conf.ini

Many critical application parameters are configured within this configuration file.  This configuration file should be installed in the same directory as mf_meals.py   

To help with managing these configurations, I also included a small python app for you to create your own config file. This app is called: meals_ ini_ set.py

___
###Database Information:##

This application utilizes SQLAlchemy ORM to persist all data in an SQL database. It is assumed that you have access to a computer running postgreSQL v9.4 or later. Whether connecting to this computer locally or remotely, you will need to connect to postgres as a superuser (such as 'postgres') and create a database called 'Meals'.
    
The Meals database must have the following roles provisioned:  
>***Database Owner:*** Group role: web  
>***Database User:*** Login role: sid  
(**most queries will be run as login role 'sid', so python application 
will not work if these roles are not provisioned correctly.**)

Once the database is created, the following file with provision the database as needed.

    try_db_create01.py



___
###Stormpath Account:###

I decided to use Strompath for my User Authentication & Authorization.  This places user account info in Stormpath's secure servers and not on mine.  

For more details on Stormpath https://docs.stormpath.com/python/quickstart/  

You can install Stormpath using pip:

    $ pip install -U stormpath

If that doesn’t work, try this instead:

    $ easy_install -U stormpath

You may need to run the above commands with sudo depending on your Python setup.

*Get an API Key*  

All requests to Stormpath must be authenticated with an API Key.

1. If you haven’t already, Sign up for Stormpath @ https://api.stormpath.com/register  You’ll be sent a verification email.
2. Click the link in the verification email.
3. Log in to the Stormpath Admin Console using the email address and password you used to register with Stormpath.
4. Click the Create API Key or Manage Existing Keys button in the middle of the page.
5. Under Security Credentials, click Create API Key.
6. This will generate your API Key and download it to your computer as an apiKey.properties file. If you open the file in a text editor, you will see something similar to the following:  

        apiKey.id = 144JVZINOF5EBNCMG9EXAMPLE
        apiKey.secret = lWxOiKqKPNwJmSldbiSkEbkNjgh2uRSNAb+AEXAMPLE  

7. Save this file in a secure location, such as your home directory, in a hidden .stormpath directory. For example:  
  
        $ mkdir ~/.stormpath
        $ mv ~/Downloads/apiKey.properties ~/.stormpath/

8. Change the file permissions to ensure only you can read this file. For example:

        $ chmod go-rwx ~/.stormpath/apiKey.properties

The apiKey.properties file holds your API key information, and can be used to easily authenticate with the Stormpath library.
Other Things You Can Do with Stormpath

In addition to user registration and login, Stormpath can do a lot more!

   - Create and manage user groups.
   - Partition multi-tenant SaaS account data.
   - Simplify social login with providers like Google and Facebook.
   - Manage developer API keys and access tokens.
   - Verify new users via email.
   - Automatically provide secure password reset functionality.
   - Centralize your user store across multiple applications.
   - Plug into your favorite web framework (like Flask!).




___
###Google Developer Account:###

For more details on using Stormpath to integrate and offer Social Login see:  
          http://flask-stormpath.readthedocs.io/en/latest/product.html#use-google-login  


**Create a Google Project**

The first thing you need to do is log into the Google Developer Console and create a new Google Project.

You can do this by visiting the Developer Console and clicking the “Create Project” button. 
Go ahead and pick a “Project Name” (usually the name of your app), and (optionally) a “Project ID”.

**Enable Google Login**

Now that you’ve got a Google Project, enable Google Login. The way Google Projects work is that you have to selectively enable what functionality each Project needs.

From your Google API Console Dashboard click on your new Project, then in the side panel click on the “APIs & auth” menu option.

Now, scroll through the API list until you see “Google+ API”, then click the “OFF” button next to it to enable it. 

**Create OAuth Credentials** 

Next create a new OAuth client ID. This is what we’ll use to handle user login with Google.

From your Console Dashboard click the “APIs & auth” menu, then click on the “Credentials” sub-menu.

You should see a button labeled “Create New Client ID” near the top of the page – click that.

You’ll want to do several things here:

1. Select “Web application” for your “Application Type”.
2. Remove everything from the “Authorized Javascript Origins” box.
3. Add the URL of your site (both publicly and locally) into the “Authorized Redirect URI” box, with URI that tells Google where to redirect users after they’ve logged in with Google.
4. Once you’ve specified your settings, go ahead and click the “Create Client ID” button.

Important: Take note of your “Client ID” and “Client Secret” variables provided by Google.

**Configure Your Flask App**

Now that we’ve created a new Google Project and generated OAuth secrets – we can now enter these secrets into our Flask app so that Flask-Stormpath knows about them.  I used a config.ini file for all my configuration settings.  So you will need to edit your copy of meals_ ini_ set.py.



___
### Finally running the python application:

1. On a Mac, open a terminal window and create a directory on your computer that you want to run Meals from and clone this repository.  

 ```git clone https://github.com/marvcode/meals.git```

 There will be two subdirectories created: 'Static' and 'Templates'  

2. Change to the directory you just created.  To confirm this, you can type `pwd` at the command line and the 
   path shown should match where you have the files stored.
   
3. Finish all account set up per the prerequisite list. After all prerequisites are completed.

4. Then, at the command line, type: `python mf_meals'


___
#Documentation

###Route Definitions in mf_meals.py

>showPublic():  
3 options on this page  
1. Create a new event  
2. list my events  
3. Search for an event (that user has been invited to)  
also, this routes checks user for authenticated and if so redirect to '/public/loggedin'
>>

>create__event(user_id):  
User is able to create a new event & add details about event  
Gather important details on user from Stormpath
>>

>list_ my_ events(user_id):  
This page should list all of this user's events  
Option : Open or contribute to any of the events  
Option: Edit an event from the list  
Option: Create a new event... redirects to '/createevent'  
Option: Delete one of their own events... redirects to '/deleteevent'  
Gather important details on user from Stormpath  
>>
    
>edit__event(user_id, evt_id):  
User has the ability to edit an event that they created.  
Gather important details on user from Stormpath  
>>

>search():  
User has the ability to search for an event based on Originator last name and event ID.  
Gather details about searching user  
>>
    
>contribute(org_ id, event_ id):  
User has the ability to contribute to an event  
Gather details about contributing user   
>>

>delete(org_ id, event_ id):
Organizer has ability to delete one of their events
Gather details about contributing user   
>>
    
>json_ evt_ details(event_id):
This route defines a REST API for getting details about an event
>>






### JSON API###

www.example.com/json/<int:event_id>/
This route defines a REST API for getting details about an event.

A HTTP request to this URI will respond with the details of an event in the database.  The details within the response will include the Event Details, the requested Items, and the committed items from guests.

Note: The event must exist so that the integer value of the event_id must be valid or an 'invalid response' will be returned.

***Example for getting details about event Id 1:***  

HTTP Request to:  

    http://localhost:5000/json/1/

returns this response:  

```
{  
  "event_details": {  
    "event name": "Marvin's Retirement Party",  
    "event state": "GA",  
    "event address": "3030 Bannister Rd",  
    "event attendee count": 22,  
    "event location": "Fulton's House",  
    "event image": "party01.jpg",  
    "event city": "Comptonville",  
    "event notes": "Wow come help us celebrate Marvin's retirement",  
    "organizer last name": "Fuller",  
    "organizer id": "P92kexample6FZpMo3omCfA",  
    "event time": "12:00 pm",  
    "organizer first name": "Marvin",  
    "event zipcode": "30088",  
    "organizer username": "marvAdmin",  
    "event date": "2016-02-14",  
    "event id": 1  
  },  
  "committed_items": [  
    {  
      "category": "Main Dish",  
      "username": "tester01",  
      "user last name": "Jasse",  
      "item name": "BBQ Pork",  
      "user first name": "Hugh",  
      "user quantity": 1,  
      "user email": "tester01@marvsprojectsite.net",  
      "user note": "I will bring a pound of smoked pulled pork.",  
      "event id": 1  
    },  
    {  
      "category": "Side Dish",  
      "username": "tester02",  
      "user last name": "Early",  
      "item name": "Green Beans",  
      "user first name": "Brighton",  
      "user quantity": 1,  
      "user email": "tester02@marvsprojectsite.net",  
      "user note": "I'll bring the green beans.",  
      "event id": 1  
    }  
  ],  
  "requested_items": [  
    {  
      "event_id": 1,  
      "requested_note": "Need some BBQ pork & Chicken",  
      "requested quantity": 2,  
      "requested_category": "Main Dish"  
    },  
    {  
      "event_id": 1,  
      "requested_note": "Need 3 side dishes",  
      "requested quantity": 3,  
      "requested_category": "Side Dish"  
    }  
  ]  
}  
```
</br>
  




#Project Grading Rubric Status:

Requirements | Comments
-------------|----------
JSON API Endpoint | Met - User must know the event ID, but a HTTP request to a 'http://localhost:5000/json/event_ID/ will provide the user with all database details for that event including requested and committed items.  
CRUD : Create | Met - User has the option to create an event and set all details for the event.  User must be logged in and authenticated for access to this page.  reads a listing of their events, reads what food has been committed by others
CRUD : Read | Met - Several ways, but one is that user has ability to read a listing of their events as what food has been committed by others.  User must be logged in and authenticated for access to this page.  
CRUD : Update | Met - The organizer of an event is provided the opportunity to edit all details about their event on the edit event screen.  User must be logged in and authenticated for access to this page.  
CRUD : Delete | Met - The organizer of an event is provided the opportunity to delete any of their own events.  User must be logged in and authenticated for access to this page.
Authorization is checked before all CRUD functions are allowed | Met - Utilized Flask-Stormpath to authorize access to each flask route.  
3rd Party Authentication | Met - leveraged Flask-Stormpath to manage user logins and authentication.  Also provided a Google+ Social Login option for user.  
Login & Logout Buttons are included | Met - Used the Bootstrap header to show the user their login status.  Yes, I offer a Login & Logout button depending on current status.
Code Quality / Ready for review | Met - Yes
Code Quality / Comments | Met - Yes, abundant comments throughout source code.
Documentation ReadME File | Met - Yes, this file.



Udacity FullStack Web Developer NanoDegree - Project Item Catalog.  
Written by: Marvin Fuller  
Started: December 26, 2015 - Completed June, 2016.  