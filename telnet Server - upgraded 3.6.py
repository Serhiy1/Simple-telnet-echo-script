import socket, threading
import datetime

HOST = ''
PORT = 23

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = []  # list of clients connected
number_of_clients = 0 # counter of clients
lock = threading.Lock()
print (PORT)
print ("server IP: ", socket.gethostbyname(socket.gethostname()))


class chatServer(threading.Thread):
    def __init__(self, socket, address, name):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.name = "client " + name
        print(self.address)

    def run(self):

        global number_of_clients
        
        lock.acquire()
        clients.append(self)
        lock.release()
        print('{:%H:%M:%S}'.format(datetime.datetime.now().time()), '%s connected.' % self.name)

        try:
            while True:

                data = self.socket.recv(1024)
                data = data.decode('ascii')

                print('{:%H:%M:%S}'.format(datetime.datetime.now().time()), self.name, ': ', data)
                if not data:
                    break
        except socket.error as error:
            print("unexpected disconnection from %s" % (self.name,))
            
        self.socket.close()
        print('{:%H:%M:%S}'.format(datetime.datetime.now().time()), '%s disconnected.' % self.name)
        lock.acquire()
        number_of_clients -= 1
        clients.remove(self)
        lock.release()


while True:  # wait for socket to connect
    # send socket to chatserver and start monitoring
    number_of_clients += 1    
    tuple = s.accept()
    chatServer(tuple[0], tuple[1], str(number_of_clients)).start()
