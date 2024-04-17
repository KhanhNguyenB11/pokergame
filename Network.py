import socket
import pickle
HOST = 'localhost'
PORT = 65432
class Network():
    def __init__(self):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        self.id=self.connect_and_join()

    def setNAR(self,room_id,name):
        self.room_id=room_id
        self.name=name
        message = f"JOIN {room_id} AS {name}"
        self.client.send(message.encode())
        data = self.client.recv(1024).decode()
        if data.find("host") != -1:
            return True
        else:
            return False


    def connect_and_join(self):
        try:
            self.client.connect((HOST,PORT))
            return 1
        except:
            pass
    def sendData(self,data):
        try:
            self.client.send(data.encode())
            data=self.client.recv(1024).decode()
            return data
        except:
            pass
    def GetObs(self,data):
        try:
            self.client.send(data.encode())
            data = self.client.recv(1024)
            data = pickle.loads(data)
            return data
        except:
            return None
