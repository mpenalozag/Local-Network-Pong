import sys

from cliente import Client
from ventana_inicio import VentanaInicio
from ventana_menu import VentanaMenu, PopUpUnirsePartida
from ventana_juego import VentanaJuego
from sala_espera import SalaEspera

from PyQt5.QtWidgets import QApplication


#Creamos primero nuestra aplicación
app = QApplication([])

#Instanciamos nuestras ventanas
initial_window = VentanaInicio()
menu_window = VentanaMenu()
sala_espera = SalaEspera()
pop_up_join_game = PopUpUnirsePartida()
ventana_juego = VentanaJuego()

#Instanciamos nuestro cliente
client = Client('localhost', 8080)

#Conectamos nuestras señales
initial_window.senal_enviar_username.connect(client.assing_username)
initial_window.senal_conectar_a_servidor.connect(client.connect_to_server)
client.senal_abrir_menu.connect(menu_window.show)
client.senal_abrir_menu.connect(initial_window.hide)
menu_window.senal_crear_partida.connect(client.crear_partida)
client.senal_crear_sala_espera.connect(sala_espera.crear_partida)
client.senal_crear_sala_espera.connect(menu_window.hide)
menu_window.senal_abrir_pop_up.connect(pop_up_join_game.show)
pop_up_join_game.senal_enviar_codigo.connect(client.unirse_partida)
client.senal_actualizar_sala_espera.connect(sala_espera.actualizar_sala_espera)
client.senal_actualizar_sala_espera.connect(menu_window.hide)
client.senal_actualizar_sala_espera.connect(pop_up_join_game.hide)
sala_espera.senal_ready_to_play.connect(client.player_ready_to_play)
client.senal_empezar_partida.connect(sala_espera.hide)
client.senal_empezar_partida.connect(ventana_juego.iniciar_pantalla)

#Creamos nuestro loop de la aplicación
sys.exit(app.exec_())