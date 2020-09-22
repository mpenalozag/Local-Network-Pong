#Cliente que sea capaz de conectarse al servidor
#Nuestro cliente tendra que heredar de QObject para comunicarse con el front-end


import socket
import json
from threading import Thread


from PyQt5.QtCore import QObject, pyqtSignal


class Client(QObject):

    senal_abrir_menu = pyqtSignal()
    senal_crear_sala_espera = pyqtSignal(dict)
    senal_actualizar_sala_espera = pyqtSignal(dict)
    senal_empezar_partida = pyqtSignal(dict)

    def __init__(self, host, port):
        super().__init__()
        self.address = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.codigo_partida = None

    def connect_to_server(self):
        try:
            self.client.connect(self.address)
            print('Conexión exitosa con el servidor')
            self.senal_abrir_menu.emit()
            thread_listen_server = Thread(target=self.listen_to_server, daemon=True)
            thread_listen_server.start()
        except ConnectionError:
            print('Error al conectarse con servidor')
            self.client.close()

    def listen_to_server(self):
        try:
            while True:
                largo_comando = int.from_bytes(self.client.recv(4), byteorder='little')
                comando = self.client.recv(largo_comando).decode()

                if comando == 'info partida creada':
                    largo_info = int.from_bytes(self.client.recv(4), byteorder='little')
                    info = json.loads(self.client.recv(largo_info))
                    self.codigo_partida = info['codigo']
                    self.asignar_partida(info)

                if comando == 'actualizar sala de espera':
                    largo_info = int.from_bytes(self.client.recv(4), byteorder='little')
                    info = json.loads(self.client.recv(largo_info))
                    info['yo'] = self.username
                    self.actualizar_sala_espera(info)

                if comando == 'partida lista':
                    largo_info = int.from_bytes(self.client.recv(4), byteorder='little')
                    info = json.loads(self.client.recv(largo_info))
                    self.iniciar_partida(info)

        except ConnectionResetError:
            print('Conexión perdida con el servidor')
        finally:
            self.client.close()
        
    def enviar_comando(self, comando):
        largo_comando = len(comando.encode()).to_bytes(4, byteorder='little')
        comando_encoded = comando.encode()
        self.client.sendall(largo_comando + comando_encoded)

    def enviar_info(self, info):
        encoded_info = json.dumps(info).encode()
        largo_info = len(encoded_info).to_bytes(4, byteorder='little')
        self.client.sendall(largo_info + encoded_info)

    def crear_partida(self):
        self.enviar_comando('crear partida')

    def assing_username(self, username):
        self.username = username
        self.enviar_comando('nuevo jugador')
        self.enviar_info(username)

    def asignar_partida(self, info):
        self.senal_crear_sala_espera.emit(info)

    def unirse_partida(self, codigo):
        self.enviar_comando('unirse a partida')
        info = dict()
        info['username'] = self.username
        info['codigo'] = codigo
        self.enviar_info(info)

    def actualizar_sala_espera(self, info_partida):
        self.senal_actualizar_sala_espera.emit(info_partida)

    def player_ready_to_play(self, info):
        self.enviar_comando('player ready to play')
        self.enviar_info(info)

    def iniciar_partida(self, info):
        self.senal_empezar_partida.emit(info)