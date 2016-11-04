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
tomm = date.replace(day=+1)
yest = date.replace(day=-1)

txt = "This is a sample text that would got into a memo"
text2 = "This is another sample text that would be in a memo"
def test_add(txt,date):
   """
   tests if date and text is added
   """
   test = add_memo(txt,date)["text"]
   
   print(test)
   assert collection.find({"text":test,"text":1,"_id":0})  == test 

def test_del():
    """
    tests if del works
	"""
    pass
    #delete_memo(text,date)
    #assert collection.find() ==