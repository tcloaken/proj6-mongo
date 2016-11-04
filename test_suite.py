#! /bin/python3
"""
nose tests for functions in flask_main
"""


### imports
import flask
from flask_main import humanize_arrow_date
from flask_main import get_memos
from flask_main import add_memo
from flask_main import delete_memo

import arrow
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


date = arrow.utcnow().floor("day")
print (date)
tomm = date.replace(hours=+24)
print (tomm)
yest = date.replace(hours=-24)

day = 24
month = day*20
txt = "This is a sample text that would go into a memo"
text2 = "This is another sample text that would be in a memo"
def test_human():
    """
    tests if dates are humanized
    """
    assert humanize_arrow_date(tomm) == "Tomorrow"
    assert humanize_arrow_date(yest) == "Yesterday"
	
def test_auto():
    """
    tests if a bunch of dates are humanized
    """
    
    assert humanize_arrow_date(tomm.replace(hours=+24)) == "Day after tomorrow"
    assert humanize_arrow_date(tomm.replace(hours=+48)) == "in {} days".format(3)
    for i in range(0,month,day):
       assert humanize_arrow_date(tomm.replace(hours=+(48+i))) == "in {} days".format((int(i/day)+3))
	   

def test_add():
   """
   tests if date and text is added
   """
   d = date.date()
   test = add_memo(d,txt)
   
   id = test["_id"]
   #find the newly made id key in the database
   check = collection.find({"_id":id}).distinct("_id")
   check = str(check[0])
   id = str(id)
   #assert that they are the same
   assert check == id
   
   #clean up
   sdate = arrow.get(date).isoformat()
   delete_memo(txt,sdate)
   

def test_del():
    """
    tests if del works
    """
	#get date in correct format
    sdate = arrow.get(date).isoformat()
    d = date.date()
	#make new database entry
    test = add_memo(d,txt)
    #hold value for id key
    id = test["_id"]
    #delete the entry
    delete_memo(txt,sdate)
    
	#try to find the deleted entry made id key in the database
    check = collection.find({"_id":id}).distinct("_id")
    
	#make sure you can't find it in the database
    assert not check
