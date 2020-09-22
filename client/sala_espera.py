from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType('sala_espera.ui')

class SalaEspera(window_name, base_class):

    senal_ready_to_play = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.codigo = None
        self.boton_start_game.clicked.connect(self.start_game)
        self.player = None
        self.num_player = None

    def crear_partida(self, info):
        self.codigo = info['codigo']
        self.codigo_match.setText(self.codigo)
        self.player1.setText(info['player1'])
        self.show()

    def actualizar_sala_espera(self, info):
        self.codigo = info['codigo']
        self.codigo_match.setText(info['codigo'])
        if info['yo'] == info['player1']:
            self.player2.setText(info['player2'])
            self.player = info['player1']
            self.num_player = 'player1'
        if info['yo'] == info['player2']:
            self.player1.setText(info['player1'])
            self.player2.setText(info['player2'])
            self.player = info['player2']
            self.num_player = 'player2'
        self.update()
        if info['yo'] == info['player2']:
            self.show()

    def start_game(self):
        info = dict()
        info['codigo'] = self.codigo
        info['player'] = self.num_player
        self.senal_ready_to_play.emit(info)