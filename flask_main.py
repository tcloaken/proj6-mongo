"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import arrow    # Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
import pymongo
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  g.memos = get_memos()
  for memo in g.memos: 
      app.logger.debug("Memo: " + str(memo))
  return flask.render_template('index.html')




@app.route("/memo_submit")
def memo_submit():
    app.logger.debug("memo submit")
    text = request.args.get("memo", type=str)
    date = request.args.get("date", type=str)
    add_memo(date, text)
    
    return index()

    

@app.route("/memo_cancel")
def memo_cancel():
    app.logger.debug("memo cancelled")
    return index()

@app.route("/del_memo")
def del_memo():
    app.logger.debug("memo deleted")
    text = request.args.get("memo", type=str)
    date = request.args.get("date", type=str)
    delete_memo(text,date)
    return index()
    
    
@app.route("/new_memo")
def new_memo():
    app.logger.debug("new memo")
    return flask.render_template('create.html')

    
@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    date = arrow.get(date).date()
    try:
        then = date
        now = arrow.utcnow().date()
        if then == now:
            human = "Today"
        else: 
            human = arrow.get(then).humanize(now)
            if human == "in a day":
                human = "Tomorrow"
            elif human == "a day ago":
                human = "Yesterday"
            
    except: 
        human = date
    return human


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        
        del record['_id']
        records.append(record)
    return sorted(records,key=sortdate)

def sortdate(el):
    """
    returns a key in dict el
    """
    return el["date"]
    
def add_memo(date,text):
    """
    Args:  date -the date of memo
           text -what the memo says
    adds memo to the database
    Returns nothing
    """
    d = arrow.get(date).isoformat()
    record = { "type": "dated_memo", 
           "date":  d,
           "text": text
          }
    collection.insert( record )
    return

def delete_memo(text,date):
    """
    Args:  
           text -what the memo says
    deletes a memo
    Returns nothing
    """
    
    for record in collection.find( { "type": "dated_memo" } ):
        if(record['text'] == text) and (record['date'] == date):
            collection.remove(record)
            break
        else:
            continue
    
    return
    
if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")

    
