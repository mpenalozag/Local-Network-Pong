from server import Server
from logica import Logic

logic = Logic()
server = Server('localhost', 8080, logic)
