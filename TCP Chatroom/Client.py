
# Client side implementation of the TCP chatroom. 
import socket 
import select 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
  
while True: 
  
    # A list of the possible input streams
    sockets_list = [sys.stdin, server] 
  
    #Either the user is sending a message, or the server is sending a message. 
    #If the input stream is user, then a user will be pulled from the socket list.
    #If the input stream is server, the else statement will evaluate. 
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print message 
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush() 
server.close() 

