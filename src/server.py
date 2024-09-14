import socket
import _thread
import pickle
from threading import Lock

from classes.player import Player
from utils.settings import Settings

settings = Settings()

server = settings.ip_address
port = settings.port

print(f"IP: {server, type(server)}")
print(f"Porta: {port, type(port)}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET é a família de endereços para IPv4
# SOCK_STREAM é o tipo de socket para TCP

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print("Erro ao iniciar o servidor. Verifique se o endereço IP está correto.")

# Número máximo de conexões que o servidor pode aceitar
s.listen(2)
print("Servidor iniciado. Aguardando conexão...")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]

connected_players = 0  # Variável para contar jogadores conectados
lock = Lock()  # Lock para evitar condições de corrida


def threaded_client(conn, player):
    global connected_players

    with lock:
        connected_players += 1
    print(f"Jogador {player} conectado. Jogadores conectados: {connected_players}")

    conn.send(
        pickle.dumps(players[player])
    )  # Envia uma mensagem de confirmação ao cliente

    # Inicializa a variável de resposta
    reply = ""

    while True:
        try:
            data = pickle.loads(
                conn.recv(2048)
            )  # 2048 é o tamanho do buffer (em bytes)
            players[player] = data

            # Se não encontrarmos dados, a conexão com o cliente foi perdida
            if not data:
                print("Desconectado")
                break
            else:
                reply = players[1] if player == 0 else players[0]

            # print("Recebido: ", data)
            # print("Enviado: ", reply)

            # Enviando a resposta de volta ao cliente (codificada em um objeto de bytes)
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print(f"Conexão perdida com jogador {player}")
    conn.close()

    with lock:
        connected_players -= 1
    print(f"Jogadores conectados restantes: {connected_players}")


while True:
    conn, addr = s.accept()  # Aceita a conexão do cliente
    print("Conectado à: ", addr)

    # Criamos uma nova thread para cada cliente para podermos
    # aceitar múltiplos clientes ao mesmo tempo (multithreading - paralelismo)
    _thread.start_new_thread(threaded_client, (conn, connected_players))
