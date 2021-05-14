import socket
import os
import argparse
from _thread import *


class Server :
    def __init__(self, clients_num) :
        self.ServerSideSocket = socket.socket( )
        self.host = '127.0.0.1'
        self.port = 5053
        self.ThreadCount = 0
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"
        self.clients_num = clients_num
        self.clients = []
        self.__create_clients__( )

    def __create_clients__(self) :
        for i in range(self.clients_num) :
            os.system("start client.py")


    def server_cycle(self) :
        try :
            self.ServerSideSocket.bind((self.host, self.port))
        except socket.error as e :
            print(str(e))

        print(f'\nServer is running y! (number of clients - {self.clients_num})\n. . .')
        self.ServerSideSocket.listen(5)

        while True :
            Client, address = self.ServerSideSocket.accept( )
            self.ThreadCount += 1
            print('\nNew client connected, address: ' + address[0] + ':' + str(address[1]) + ' thread no. ' + str(
                self.ThreadCount))
            start_new_thread(self.multi_threaded_client, (Client,))

        ServerSideSocket.close( )

    def multi_threaded_client(self, connection) :
        connection.send(str.encode(f'{self.ThreadCount}'))
        while True :
            received = connection.recv(self.BUFFER_SIZE).decode( )
            filename, filesize, option = received.split(self.SEPARATOR)
            if option == '1' :
                print("\nReceiving . . .")
                filename = os.path.basename(filename)
                filename = 'server/' + filename
                with open(filename, "wb") as f :
                    offset = 0
                    while True :
                        bytes_read = connection.recv(self.BUFFER_SIZE)
                        if not bytes_read :
                            break
                        f.write(bytes_read)
                        if offset % 2 :
                            current_filesize += self.BUFFER_SIZE
                        else :
                            current_filesize = os.path.getsize(filename)
                        if abs(int(filesize) - int(current_filesize)) <= self.BUFFER_SIZE :
                            break
                        offset += 1

                    print(f"\nSuccesfully received {filename} and saved in server's folder")

            elif option == '0' :
                print("\nSending . . .")
                filesize = os.path.getsize(filename)
                connection.send(f"{filename}{self.SEPARATOR}{filesize}".encode( ))
                with open(filename, "rb") as f :
                    while True :
                        bytes_read = f.read(self.BUFFER_SIZE)
                        if not bytes_read :
                            break
                        connection.send(bytes_read)

                print(f"\nSuccesfully sent {filename} to the client")


parser = argparse.ArgumentParser( )
parser.add_argument("clients_num", help="set number of clients", type=int)
args = parser.parse_args( )

server = Server(args.clients_num)
server.server_cycle( )
