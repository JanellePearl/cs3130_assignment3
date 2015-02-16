CS3130
Assignment 3
Janelle Montgomery

This is a python program that will set up a UDP connection in the form of a messenger. In order to start the program you must supply whether or not you want to set up the client or the server. ex.) jmsg.py client or jmsg.py server
If you are the client you will get a list of commands that the user may enter.
My messenger requires an 'active' user meaning someone has signed in and is verified in the user database. If you want to signin as someone else you can signout and signin as another authorized user. 
When the user signs in their messages will show up, these are messages that have been sent when the user was offline.
The messages have a msg id of 1-100 so the document will only store a finite amount of messages before they must be deleted.
The client will be able to view the users and their status.
The client will also be able to message a user by supplying their user id. If the user is online they will send a message and wait for a response before they can continue to message another person or the same person.

Assumptions:
- the user database has existing users in the proper format
- the message database has at least the starter flag in it
 