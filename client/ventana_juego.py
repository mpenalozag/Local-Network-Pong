from PyQt5 import uic

window_name, base_class = uic.loadUiType('ventana_juego.ui')

class VentanaJuego(window_name, base_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def iniciar_pantalla(self, info):
        self.nombre_p1.setText(info['player1'])
        self.nombre_p2.setText(info['player2'])
        self.show()