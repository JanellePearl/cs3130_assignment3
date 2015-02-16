#cs3130 Assignment 3
#Janelle Montgomery
#Setting up a UDP client that will read from a database of users.
#Database,Client and Server

import socket, sys, argparse
import main
from random import randint

MAX_BYTES = 65535
#global client id so the server knows who is talking
CLIENT_ID = 0


#the server waits for a message from the client
def server(port):
    d = users()
    #create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #bind the socket to the hostname and port
    host = ('127.0.0.1')
    sock.bind((host,port))
    print('Listening at', sock.getsockname())
    i = 1
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        #this if statement breaks up my data..formatting purposes
        if(i==1):
            print('{} says: '.format(text))
            i = 2
        
        else:
            print('{}'.format(text))
            i = 1
            #allows the server to respond once
            print('Respond with: ')
            #text= raw_input()
            text = input()
            sock.sendto(text.encode('ascii'), address)
            i=1
        

        
#The client is designed as the user. It will accept user commands and interpret
#them from main.py. It will then set up the message with the server if the user
#wants to chat.
def client(port):
    #show the client the display commands
    p = port
    main.start()
    print("-----******-----")
    print("To begin please signin as an active user :)")
    signin()
    correct = False
    while not correct:
        #accept user selection
        #selection = raw_input()
        selection = input()
        print("-----******-----")
        #carry out command
        if selection == ('signin'):
            signin()
        elif selection == ('users'):
            listusers()
        elif selection == ('message'):
            message(p)
        elif selection == ('signout'):
            signout()
        elif selection == ('exit'):
            leave()
        else:
            print('Your selection is not valid please try again.')
        
   

#check if the user is authorized, ie. in the database. Change their status to online
def signin():
    d = users()
    m = messages()
    user = []
    print("Please enter your unique 1-4 digit user Id: ")
    #user_id = raw_input()
    user_id = input()
    if not user_id in d.keys():
        print("This user is not authorized to use Janelle Messenger!.")    
        print("\n")
        signin()
        
    #change the users status to online in the database        
    else:
        user_name = d[user_id][0]
        user.append(user_name)
        status = 'Online'
        user.append(status)
        d[user_id] = user
        print('User Id: ' + user_id + ' Username:'+user_name+' Status:'
                                  + status)
                
        with open("database.txt", "w+")as f:
            for k,v in d.items():
                f.write(k + ":" + ":".join(v) + "\n")
    
        #this checks for messages
        #goes through message database and prints off messages for client
        #if user has no messages no message will appear
        print('\nMessages: ')
        for k in m.keys():
            sentto = m[k][0]
            sentfrom = m[k][1]
            msg = m[k][2]
            if sentto == user_id:
                sendname = d[sentfrom][0]
                print(sendname + ' said: ' + msg +'\n')
                        
        
                    
                    
        global CLIENT_ID
        CLIENT_ID = user_id
            
        print("\nWaiting for next command: ")
        
#list users and their status        
def listusers():
    d = users()
    for k in d.keys():
        print('ID:' + k + ' Username:' + d[k][0] + ' Status:'+d[k][1])
            
    print("\nWaiting for next command: ")   
   
        
    
#Allow user to signout, set status to offline           
def signout():
    d = users()
    user = []
    print('Signed out: ')
    user_id = CLIENT_ID
    user_name=d[user_id][0] 
    user.append(user_name)
    status = 'Offline'
    user.append(status)
    d[user_id] = user
    with open("database.txt", "w+")as f:
            for k,v in d.items():
                f.write(k + ":" + ":".join(v) + "\n")
                       
    print('User Id: ' + user_id + ' Username:'+user_name+' Status:'
                            + status)
    print('\nPlease sign in to continue using messenger :)\n')
    signin()
    
    

#exit the program    
def leave():
    exit(0)

#this is the client portion where the user can send a message    
def message(port):
    d = users()
    m = messages()
    #create a UDP socket for the client

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Please enter the user Id of who you want to message.')
    chat_id = input()
    #chat_id = raw_input()
    
    if not chat_id in d.keys():
        print('\nWhoops try again!')
        
    else:
        client = CLIENT_ID
        clientname = d[client][0]
        username = d[chat_id][0]
        print('send ' + username + ': ')
        #text = raw_input()
        text = input()
        
    #checks to see if user is offline before sending message   
    if (d[chat_id][1]=="Offline"):
        #creates a random int from 1-100 for message id
        msgid = randint(1,100)
        f = open('messages.txt','a')
        #message is saved to message database
        f.write("{}:".format(msgid) + chat_id + ":" + client + ":" + text + "\n")
        print("User is offline and your message will be saved.")
                    
    else:
        data = text.encode('ascii')
        clientname = clientname.encode('ascii')
        delay = 0.1
        #client attempts to send message to the server
        sock.sendto(clientname,('127.0.0.1', port))
        sock.sendto(data,('127.0.0.1', port))
            
        data, address = sock.recvfrom(MAX_BYTES) # Danger!
        #text = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('{} replied: {}'.format(username, text))
                    
                
            
    print("\nWaiting for next command: ")
        
    
#opens and reads from the user data base (user id:username:status)            
def users():
    d = {}
    f=open("database.txt","r")
    for user in f:
        user=user.strip()
        ID,name = user.split(":",1)
        d[ID]=name.split(":",2)

    return d

#opens and reads from the message database (msgid:sentto:sentfrom:msg)
def messages():
    m = {}
    f=open("messages.txt","r")
    for user in f:
        user=user.strip()
        ID,name = user.split(":",1)
        m[ID]=name.split(":",3)

    return m
    
  
        
if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
    ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
