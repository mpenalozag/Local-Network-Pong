import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType('ventana_inicio.ui')

class VentanaInicio(window_name, base_class):

    senal_conectar_a_servidor = pyqtSignal()
    senal_enviar_username = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_jugar.clicked.connect(self.conectar_a_servidor)
        self.show()

    def conectar_a_servidor(self):
        self.senal_conectar_a_servidor.emit()
        self.senal_enviar_username.emit(self.username.text())

if __name__ == '__main__':
    app = QApplication([])
    ventana_inicio = VentanaInicio()
    sys.exit(app.exec_())
