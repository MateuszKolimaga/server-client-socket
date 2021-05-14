import socket
import os

class Client():
    def __init__(self):
        self.ClientMultiSocket = socket.socket( )
        self.host = '127.0.0.1'
        self.port = 5053
        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<SEPARATOR>"

    def client_cycle(self):
        try :
            self.ClientMultiSocket.connect((self.host, self.port))
        except socket.error as e :
            print(str(e))

        res = self.ClientMultiSocket.recv(self.BUFFER_SIZE)
        print('## Numer klienta ' + res.decode('utf-8') + " ##")

        while True :
            Input = input('\n[0] - Download file from the server \n[1] - Send file to server \n\nEnter option number: ')
            if int(Input) :
                filename = input(
                    "\nEnter the file path to be sent to the target or press Enter to send the default file.: ")
                if filename :
                    self.send_file(filename)
                else :
                    self.send_file( )
            else :
                filename = input(
                    "\nEnter the file path to be sent to the target or press Enter to send the default file.: ")
                if filename :
                    self.download_file(filename)
                else :
                    self.download_file( )
        self.ClientMultiSocket.close( )

    def send_file(self, filename = 'client/doc_client.doc') :
        filesize = os.path.getsize(filename)
        option = 1
        self.ClientMultiSocket.send(f"{filename}{self.SEPARATOR}{filesize}{self.SEPARATOR}{option}".encode( ))
        with open(filename, "rb") as f :
            while True :
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read :
                    break
                self.ClientMultiSocket.sendall(bytes_read)
        print(f"\n Succesfully sent {filename} to the server")

    def download_file(self, _filename='server/doc_server.doc') :
        filesize = option = 0
        self.ClientMultiSocket.send(f"{_filename}{self.SEPARATOR}{filesize}{self.SEPARATOR}{option}".encode( ))

        received = self.ClientMultiSocket.recv(self.BUFFER_SIZE).decode( )
        filename, filesize = received.split(self.SEPARATOR)
        base_filename = os.path.basename(filename)
        filename = f'client/' + base_filename

        with open(filename, "wb") as f :
            offset = 0
            while True :
                bytes_read = self.ClientMultiSocket.recv(self.BUFFER_SIZE)
                if not bytes_read :
                    break
                f.write(bytes_read)

                if offset % 2 :
                    current_filesize += self.BUFFER_SIZE
                else :
                    current_filesize = os.path.getsize(filename)
                if abs(int(filesize) - int(current_filesize)) <= self.BUFFER_SIZE:
                    break

            print(f"\nSuccesfully received {base_filename} and saved in client's folder\n")

client = Client()
client.client_cycle()
