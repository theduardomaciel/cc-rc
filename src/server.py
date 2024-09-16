import socket
import pygame
import pickle
import _thread
from random import randrange, randint
from threading import Lock

from classes.match import Match
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

match = Match(0)  # Inicializa a partida
lock = Lock()  # Lock para evitar condições de corrida


def generate_player(id: int) -> Player:
    random_position = randrange(0, settings.width - 50), randrange(
        0, settings.height - 50
    )
    random_color = (
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )

    return Player(id, random_position[0], random_position[1], 50, 50, random_color)


# Função para lidar com a conexão de um cliente (cada cliente é uma thread separada)
def threaded_client(conn, player):
    global match

    with lock:
        match.connected_players += 1
    print(
        f"Jogador {player} conectado. Jogadores conectados: {match.connected_players}"
    )

    with lock:
        # Garantir que a operação de adicionar jogadores à lista é segura
        if match.connected_players <= match.max_players:
            match.add_player(generate_player(player))
        else:
            return

    print("Jogador atual: ", player)
    print("Jogadores: ", match.players)

    # Enviamos os dados do jogador atual para o cliente
    conn.send(pickle.dumps(match.players[player]))

    while True:
        try:
            # Obtemos os dados atualizados do cliente (jogador atual)
            data = pickle.loads(conn.recv(2048))

            # Se não encontrarmos dados, a conexão com o cliente foi perdida
            if not data:
                break
            else:
                # Caso um jogador tenha entrado, verificamos se a partida pode ser iniciada
                if match.state == "waiting" and match.connected_players > 1:
                    print("Agendando partida...")
                    match.schedule_intermission()

                if data == "reset":
                    match.start()
                else:
                    # Atualizamos os dados do jogador atual
                    match.players[player] = data

            # Verifica se o intervalo entre partidas acabou
            if match.state == "intermission" and match.connected_players > 1:
                match.check_intermission_timer()

            # print("Recebido: ", data)
            # print("Enviado: ", reply)

            # Enviando a resposta de para todos os clientes com os dados atualizados
            conn.sendall(pickle.dumps(match))
        except:
            break

    print(f"Conexão perdida com jogador {player}")
    conn.close()

    with lock:
        match.remove_player(match.players[player])
        match.connected_players -= 1
    print(f"Jogadores conectados restantes: {match.connected_players}")


while True:
    conn, addr = s.accept()  # Aceita a conexão do cliente
    print("Conectado à: ", addr)

    with lock:
        player_id = match.connected_players  # Atribui um ID ao jogador atual

    # pygame.time.get_ticks() = current_time
    time_since_last_intermission = (
        pygame.time.get_ticks() - match.last_intermission_time
    )

    # Criamos uma nova thread para cada cliente, visto que podemos
    # aceitar múltiplos clientes ao mesmo tempo (multithreading - paralelismo)
    _thread.start_new_thread(threaded_client, (conn, player_id))
