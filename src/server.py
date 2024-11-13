import socket
import pygame
import pickle
import _thread

from threading import Lock

from classes.match import Match
from utils.settings import Settings

settings = Settings()

server = settings.ip_address
port = settings.port

print(f"IP: {server, type(server)}")
print(f"Porta: {port, type(port)}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET é a família de endereços para IPv4
# SOCK_STREAM é o tipo de socket para TCP (SOCK_DGRAM para UDP)

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


# Função para lidar com a conexão de um cliente (cada cliente é uma thread separada)
def threaded_client(conn, player):
    global match

    # Primeira conexão com o cliente ========================

    with lock:
        match.connected_players += 1
    print(
        f"Jogador {player} conectado. Jogadores conectados: {match.connected_players}"
    )

    with lock:
        # Garantir que ainda existe espaço na partida para adicionar um novo jogador
        if match.connected_players <= match.max_players:
            match.add_player(match.generate_player(player))
        else:
            print("Partida cheia. Não é possível adicionar mais jogadores.")
            conn.close()
            return

    print("Jogador atual: ", player)
    print("Jogadores: ", match.players)

    # Enviamos os dados do jogador atual para o cliente
    conn.send(pickle.dumps(match.players[player]))

    # Loop para manter a conexão com o cliente ========================

    tick = pygame.time.get_ticks()

    while True:
        try:
            # Obtemos os dados atualizados do cliente (jogador atual)
            data = pickle.loads(conn.recv(2048))

            ready_players = [player for player in match.players if player.is_ready]

            # Se não encontrarmos dados, a conexão com o cliente foi perdida
            if not data:
                break
            else:
                # Caso um jogador tenha entrado, verificamos se a partida pode ser iniciada
                if (
                    match.state == "idle"
                    and len(ready_players) >= settings.min_players
                ):
                    print("Iniciando partida em alguns segundos!...")
                    match.state = "waiting"
                    match.schedule_intermission()

                if data == "reset":
                    match.start()
                elif data is not None:
                    # print("Atualizando dados do jogador ", player)

                    # Atualizamos os dados do jogador atual
                    match.players[player] = data

            # Verifica se a quantidade de jogadores vivos é menor que 2
            if match.state == "running":
                match.check_game_over()

            # Verifica se a partida deve começar (intervalo acabou)
            if (
                match.state == "waiting" or match.state == "ended"
            ) and match.check_intermission_timer():
                if len(ready_players) >= settings.min_players:
                    match.start()
                else:
                    match.state = "idle"

            match.remaining_intermission_time = (
                match.intermission_duration - (pygame.time.get_ticks() - match.last_intermission_time)
            )

            # print("Recebido: ", data)
            # print("Enviado: ", reply)

            # Enviando a resposta de para todos os clientes com os dados atualizados
            conn.sendall(pickle.dumps(match))
        except:
            break

    # Se a conexão com o cliente foi perdida, fechamos a conexão e removemos o jogador

    print(f"Conexão perdida com jogador {player}")
    conn.close()

    with lock:
        match.remove_player(match.players[player - 1])
        match.connected_players -= 1

    print(f"Jogadores conectados restantes: {match.connected_players}")


while True:
    conn, addr = s.accept()  # Aceita a conexão do cliente
    print("Conectado à: ", addr)

    with lock:
        player_id = match.connected_players  # Atribui um ID ao jogador atual
        
    # Criamos uma nova thread para cada cliente, visto que podemos
    # aceitar múltiplos clientes ao mesmo tempo (multithreading - paralelismo)
    _thread.start_new_thread(threaded_client, (conn, player_id))
