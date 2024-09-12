import socket
import _thread
import sys
from utils.settings import Settings

settings = Settings()

server = settings.ip_address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET is the address family for IPv4
# SOCK_STREAM is the socket type for TCP

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# s.listen(2) means that the server can only accept 2 connections
s.listen(2)
print("Servidor iniciado. Aguardando conexão...")


def threaded_client(conn):
    conn.send(str.encode("Conectado"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)  # 2048 é o tamanho do buffer (em bytes)
            reply = data.decode("utf-8")  # Decodificamos a mensagem recebida

            # Se não encontrarmos dados, a conexão com o cliente foi perdida
            if not data:
                print("Desconectado")
                break
            else:
                print("Recebido: ", reply)
                print("Enviando: ", reply)

            # Enviando a resposta de volta ao cliente (codificada em um objeto de bytes)
            conn.sendall(str.encode(reply))
        except:
            break

    print("Conexão perdida")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Conectado à: ", addr)

    # Criamos uma nova thread para cada cliente, para que possamos
    # aceitar múltiplos clientes ao mesmo tempo (multithreading - paralelismo)
    _thread.start_new_thread(threaded_client, (conn,))
