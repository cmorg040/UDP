
# Python program to implement a TCP based chat room. This file implements the server side of the application. 
import socket 
import select 
import sys 
from thread import *


#AF_INET is the address of the address domain of the scoket.
#We use AF_INET whenever an internet domain has two hosts.
#
#SOCK_STREAM indicates that the data or characters to be read will be read in a continous stream.  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
#Input validation, makes sure that the proper number of arguments have been provided. 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
    exit() 
  
#The first command line argument will be read as the IP address. 
IP_address = str(sys.argv[1]) 
  
#The second command line arguent will be read as the port number. 
Port = int(sys.argv[2]) 
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
#Bind the server to the input IP address and the input Port number(arguments read above)
#Note: Make sure that the client part of the application knows about these arguments. 
server.bind((IP_address, Port)) 
  
#Listen for 100 connections
server.listen(100) 
  
list_of_clients = [] 
  
def clientthread(conn, addr): 
  
    # Send a welcome message to the client. 
    conn.send("Welcome to this chatroom!") 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
  
                    #Print user information(Address) and the accompanying message.
                    print "<" + addr[0] + "> " + message 
  
                    # Sends the message to all users in the chatroom(With the above information attached)
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 
  
                else: 
                    #If there is no message, remove the connection.
                    remove(conn) 
  
            except: 
                continue
  
#Broadcast function sends the message to all clients except the sender(who obviously doesn't need to receive it again)
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
  
                # If client disconnects, remove their connection from the server. 
                remove(clients) 
  
#Simple function for removing the client from the server's object list. 
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  

    #Accept two arguments: The socket for the connection(client), andt he IP address of the client.
    conn, addr = server.accept() 
  

    #A list of clients to keep track of who receives broadcast messages. 
    list_of_clients.append(conn) 
  
    # When a user connects, prints their IP Address. 
    print addr[0] + " connected"
  
    # Each user gets their own thread when they connect. 
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 

