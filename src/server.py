import socket
import _thread
import pickle
from random import randrange, randint
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

connected_players = 0  # Variável para contar jogadores conectados
players = list()  # Lista de jogadores conectados
lock = Lock()  # Lock para evitar condições de corrida


# Função para lidar com a conexão de um cliente (cada cliente é uma thread separada)
def threaded_client(conn, player):
    global connected_players, players

    with lock:
        connected_players += 1
    print(f"Jogador {player} conectado. Jogadores conectados: {connected_players}")

    random_position = randrange(0, settings.width - 50), randrange(
        0, settings.height - 50
    )
    random_color = (
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )

    with lock:
        # Garantir que a operação de adicionar jogadores à lista é segura
        players.append(
            Player(player, random_position[0], random_position[1], 50, 50, random_color)
        )

    print("Jogador atual: ", player)
    print("Jogadores: ", players)

    # Enviamos os dados do jogador atual para o cliente
    conn.send(pickle.dumps(players[player]))

    # Inicializa a variável de resposta
    reply = ""

    while True:
        try:
            # Obtemos os dados do cliente (jogador atual)
            data = pickle.loads(
                conn.recv(2048)
            )  # 2048 é o tamanho do buffer (em bytes)
            players[player] = data

            # Se não encontrarmos dados, a conexão com o cliente foi perdida
            if not data:
                break
            else:
                # Atualizar os dados do jogador atual
                players[player] = data

                # Enviar a lista de jogadores atualizada (exclui o jogador atual da resposta)
                reply = [p for i, p in enumerate(players) if i != player]

            # print("Recebido: ", data)
            # print("Enviado: ", reply)

            # Enviando a resposta de volta ao cliente (codificada em um objeto de bytes)
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print(f"Conexão perdida com jogador {player}")
    conn.close()

    with lock:
        players.pop(player)  # Remover o jogador da lista ao desconectar
        connected_players -= 1
    print(f"Jogadores conectados restantes: {connected_players}")


while True:
    conn, addr = s.accept()  # Aceita a conexão do cliente
    print("Conectado à: ", addr)

    with lock:
        player_id = connected_players  # Atribui um ID ao jogador atual

    # Criamos uma nova thread para cada cliente, visto que podemos
    # aceitar múltiplos clientes ao mesmo tempo (multithreading - paralelismo)
    _thread.start_new_thread(threaded_client, (conn, player_id))
