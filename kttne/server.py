import socket
import _thread
import pickle

from utils.settings import Settings

settings = Settings()

server = settings.ip_address
port = settings.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET é a família de endereços para IPv4
# SOCK_STREAM é o tipo de socket para TCP

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)  # Número máximo de conexões que o servidor pode aceitar
print("Servidor iniciado. Aguardando conexão...")


def threaded_client(conn):
    conn.send(str.encode("Conectado"))  # Envia uma mensagem de confirmação ao cliente

    # Inicializa a variável de resposta
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
            conn.sendall(pickle.dumps(reply))
        except:
            print("Erro")
            break

    print("Conexão perdida")
    conn.close()


while True:
    conn, addr = s.accept()  # Aceita a conexão do cliente
    print("Conectado à: ", addr)

    # Criamos uma nova thread para cada cliente para podermos
    # aceitar múltiplos clientes ao mesmo tempo (multithreading - paralelismo)
    _thread.start_new_thread(threaded_client, (conn,))
