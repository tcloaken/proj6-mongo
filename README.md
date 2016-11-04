# proj6-mongo
Simple list of dated memos kept in MongoDB database
Author: Trevor Enright, tenright@uoregon.edu

## What is here

A simple Flask app that displays all the dated memos it finds in a MongoDB database.
Theres a subdirectory called "secrets" and place two files
in it: 

- secrets/admin_secrets.py holds configuration information for your MongoDB
  database, including the administrative password.  
= secrets/client_secrets.py holds configuration information for your
  application. 


The client information must be created in the database for it to work
## Functionality 

The user may can add dated memos from a separate page (create.html). 
Memos are displayed in date order in the index.html where the user 
can delete memos as well. 
