from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QTextCharFormat

window_name, base_class = uic.loadUiType('ventana_menu.ui')
popup_name, popup_class = uic.loadUiType('ingresar_partida_pop_up.ui') 

class VentanaMenu(window_name, base_class):

    senal_crear_partida = pyqtSignal()
    senal_abrir_pop_up = pyqtSignal() #Esta señal emite el código de la partida

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_crear_partida.clicked.connect(self.crear_partida)
        self.boton_unirse_partida.clicked.connect(self.unirse_partida)

    def crear_partida(self):
        self.senal_crear_partida.emit()

    def unirse_partida(self):
        self.senal_abrir_pop_up.emit()


class PopUpUnirsePartida(popup_name, popup_class):

    senal_enviar_codigo = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ingresar.clicked.connect(self.unirse_partida)
    
    def unirse_partida(self):
        codigo = self.codigo.text()
        self.senal_enviar_codigo.emit(codigo.upper())

