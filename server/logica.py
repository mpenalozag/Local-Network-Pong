#La clase lógica se encargará de todos los procesos back-end del juego.

from funciones_utiles import generador_codigo_partida


class Logic:
    def __init__(self):
        self.usuarios = dict()
        self.partidas = dict()

    def crear_partida(self, player1):
        codigo_partida = generador_codigo_partida()
        while codigo_partida in self.partidas:
            codigo_partida = generador_codigo_partida()
        self.partidas[codigo_partida] = dict()
        self.partidas[codigo_partida]['state_p1'] = 'Not Ready'
        self.partidas[codigo_partida]['state_p2'] = 'Not Ready'
        self.partidas[codigo_partida]['llena'] = False
        self.partidas[codigo_partida]['player1'] = player1
        self.partidas[codigo_partida]['player2'] = None
        return codigo_partida

    def info_partida(self, codigo_partida):
        #Retonará un dict con la info de una partida
        info = dict()
        info['codigo'] = codigo_partida
        info['player1'] = self.partidas[codigo_partida]['player1']
        info['player2'] = self.partidas[codigo_partida]['player2']
        return info

    def agregar_player2_a_partida(self, codigo_partida, player2):
        self.partidas[codigo_partida]['player2'] = player2
        self.partidas[codigo_partida]['llena'] = True

    def return_client_by_username(self, nombre_usuario):
        for key, item in self.usuarios.items():
            if item == nombre_usuario:
                return key

    def player_ready_to_play(self, codigo_partida, player):
        print(player)
        if player == 'player1':
            self.partidas[codigo_partida]['state_p1'] = 'Ready'
        if player == 'player2':
            self.partidas[codigo_partida]['state_p2'] = 'Ready'

    def check_match(self, codigo_partida):
        state_player1 = self.partidas[codigo_partida]['state_p1']
        state_player2 = self.partidas[codigo_partida]['state_p2']
        if state_player1 == 'Ready' and state_player2 == 'Ready':
            print('hola')
            return True
