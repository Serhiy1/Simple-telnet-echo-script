#!C:\Python27\python.exe

import socket, threading
import datetime 
HOST = ''
PORT = 23 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = []  # list of clients connected
number_of_clients = 0
lock = threading.Lock()
print PORT
print "server IP: " , socket.gethostbyname(socket.gethostname())


class chatServer(threading.Thread):
    def __init__(self, (socket, address), name):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.name = "client " + name
        print self.address

    def run(self):
        global number_of_clients 
        lock.acquire()
        clients.append(self)
        lock.release()
        print 'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), ':%s connected.' % self.name
        
        try:
            while True:
                data = self.socket.recv(1024)
                print 'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), self.name ,'\n', data
                if not data:
                    break
        except socket.error as error:
            print "unexpected disconnection from %s" % (self.name,)




        self.socket.close()
        print 'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), ':%s disconnected.' % self.name
        lock.acquire()
        number_of_clients -= 1
        clients.remove(self)
        lock.release()
        
while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    number_of_clients += 1    
    # client = str(len(clients))
    chatServer(s.accept(), str(number_of_clients)).start()


# Source for most of this code can be found here: http://stackoverflow.com/questions/6487772/simple-telnet-chat-server-in-python

    
