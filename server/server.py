#Queremos crear un servidor que se encargue de recibir a los jugadores
#Solo nos enfocaremos en eso por ahora


import socket
import json
from threading import Thread


class Server:
    def __init__(self, host, port, logica):
        self.logic = logica
        self.address = (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()

        constant_listening = Thread(target=self.listen_for_clients, daemon=True)
        constant_listening.start()

        self.online()
    
    def online(self):
        while True:
            pass

    def bind_and_listen(self):
        self.server.bind(self.address)
        self.server.listen()
        print('Servidor esperando conexiones...')

    def listen_for_clients(self):
        while True:
            client, address = self.server.accept()
            print(f'Conexión aceptada correctamente desde {address}')
            client_thread = Thread(target=self.listen_to_specific_client, args=(client, ), daemon=True)
            client_thread.start()

    def listen_to_specific_client(self, client):
        try:
            while True:
                largo_comando = int.from_bytes(client.recv(4), byteorder='little')
                comando = client.recv(largo_comando).decode()
                
                if comando == 'nuevo jugador':
                    largo_info = int.from_bytes(client.recv(4), byteorder='little')
                    info = json.loads(client.recv(largo_info))
                    self.agregar_nuevo_jugador(info, client)

                if comando == 'crear partida':
                    codigo_partida = self.logic.crear_partida(self.logic.usuarios[client])
                    info_partida = self.logic.info_partida(codigo_partida)
                    self.enviar_comando(client ,'info partida creada')
                    self.enviar_info(client, info_partida)

                if comando == 'unirse a partida':
                    largo_info = int.from_bytes(client.recv(4), byteorder='little')
                    info = json.loads(client.recv(largo_info))
                    self.agregar_jugador_partida(info)
                    self.actualizar_sala_espera(info['codigo'])

                if comando == 'player ready to play':
                    largo_info = int.from_bytes(client.recv(4), byteorder='little')
                    info = json.loads(client.recv(largo_info))
                    self.player_ready_to_play(info)

                    

        except ConnectionResetError:
            print('Conexión perdida con cliente')
        finally:
            print('Cerrando socket del cliente')
            client.close()

    def enviar_comando(self, client, comando):
        largo_comando = len(comando.encode()).to_bytes(4, byteorder='little')
        comando_encoded = comando.encode()
        client.sendall(largo_comando + comando_encoded)

    def enviar_info(self, client, info):
        encoded_info = json.dumps(info).encode()
        largo_info = len(encoded_info).to_bytes(4, byteorder='little')
        client.sendall(largo_info + encoded_info)

    def agregar_nuevo_jugador(self, username, client):
        self.logic.usuarios[client] = username

    def agregar_jugador_partida(self, info):
        self.logic.agregar_player2_a_partida(info['codigo'], info['username'])

    def actualizar_sala_espera(self, codigo_partida):
        partida = self.logic.partidas[codigo_partida]
        partida['codigo'] = codigo_partida
        cliente_1 = self.logic.return_client_by_username(partida['player1'])
        self.enviar_comando(cliente_1, 'actualizar sala de espera')
        self.enviar_info(cliente_1, partida)
        cliente_2 = self.logic.return_client_by_username(partida['player2'])
        self.enviar_comando(cliente_2, 'actualizar sala de espera')
        self.enviar_info(cliente_2, partida)

    def player_ready_to_play(self, info):
        codigo_partida = info['codigo']
        player = info['player']
        self.logic.player_ready_to_play(codigo_partida, player)
        print(self.logic.check_match(codigo_partida))
        if self.logic.check_match(codigo_partida):
            partida = self.logic.partidas[codigo_partida]
            cliente_1 = self.logic.return_client_by_username(partida['player1'])
            self.enviar_comando(cliente_1, 'partida lista')
            self.enviar_info(cliente_1, partida)
            cliente_2 = self.logic.return_client_by_username(partida['player2'])
            self.enviar_comando(cliente_2, 'partida lista')
            self.enviar_info(cliente_2, partida)