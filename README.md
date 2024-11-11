# Dash Muse

<picture>
  <img alt="Capa para o repositório do jogo Dash Muse, desenvolvido para a matéria de Rede de Computadores" src="/.github/cover.png">
</picture>

**Dash Muse** é um jogo dinâmico multiplayer, desenvolvido em Python, onde os jogadores competem para se tornar o último sobrevivente em uma arena baseada em física e colisões.  
O jogo foi desenvolvido como projeto final da matéria Rede de Computadores do curso de Ciência da Computação da Universidade Federal de Alagoas (UFAL), e envolve habilidades de estratégia e reflexo, permitindo que os jogadores promovam ou evitem colisões enquanto permanecem dentro de uma área restrita.

## 🕹️ Sobre

No **Dash Muse**, o objetivo é empurrar outros jogadores para fora da área de jogo, causando-lhes dano.  
Os jogadores começam com 10 vidas (valor configurável) e podem realizar um dash (impulso) a cada 0,5s (500ms) para aumentar as chances de empurrar os inimigos.  

## 🛠 Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| **Python** | Linguagem principal do desenvolvimento, desde a lógica do jogo até a manutenção do servidor. |
| **Pygame** | Biblioteca para renderização gráfica e manipulação da interface, permitindo atualizações em tempo real dos jogadores. |
| **Socket** | Utilizada para configurar a conexão cliente-servidor, possibilitando o multiplayer em rede local. |
| **Pickle** | Gerenciamento de objetos serializados para envio dos dados dos jogadores. |
| **Threading** | Gerencia as conexões, monitorando eventos e mantendo a comunicação entre cliente e servidor. |

## 📂 Estrutura do Código

```plaintext
├── settings.ini             # Configurações de tela, regras do jogo e rede
├── requirements.txt         # Bibliotecas necessárias para o projeto
├── src/
│   ├── classes/             # Componentes e classes para a interface cliente
│   │   ├── player.py        # Classe com definição de atributos e eventos do jogador
│   │   └── ...              # Outras classes de componentes
│   ├── utils/               # Funções auxiliares para renderização e formatação
│   │   └── ...              # Scripts utilitários
│   ├── network.py           # Configuração de rede e dados de conexão
│   ├── client.py            # Interface e lógica do jogo, renderização dos sprites
│   └── server.py            # Servidor, gerencia partidas e conexão de jogadores
└── readme.md                # Documentação do projeto
```

## 🚀 Como Executar

Recomenda-se criar um ambiente virtual para executar o projeto em Python, mas essa etapa é opcional.

1. **Criar e ativar o ambiente virtual:**
   ```bash
   python3 -m venv env
   ```
   Ativar o ambiente:
   - **Windows:** `env\Scripts\activate`
   - **Linux/macOS:** `source env/bin/activate`

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o jogo no Visual Studio Code:**
   - Abra a pasta raiz do projeto no VS Code.
   - Pressione `Ctrl + Shift + B` e escolha a opção de execução desejada.

## 👀 Demonstrações

### Interfaces do Jogo

- **Menu Inicial:** Tela de boas-vindas.
    <picture>
    <img alt="Print do menu inicial" src="/.github/menu.png">
    </picture>
- **Sala de Espera:** Espera por pelo menos um jogador para iniciar a partida.
    <picture>
    <img alt="Print da sala de espera pela quantidade de jogadores suficientes" src="/.github/waiting_room.png">
    </picture>
- **Sala de espera por partida:** Espera alguns segundos para que outros jogadores tenham a oportunidade de se juntar à partida.
    <picture>
    <img alt="Print da sala de espera pelo início da partida após quantidade mínima de jogadores" src="/.github/intermission.png">
    </picture>
- **Tela de Partida:** Arena onde ocorre o confronto até restar apenas um jogador.
    <picture>
    <img alt="Print da tela de partida, onde o jogo ocorre" src="/.github/match.png">
    </picture>

### Exemplo de partida

https://github.com/user-attachments/assets/9e0d5e84-e444-45c5-949d-49594bb74479


## 📄 Licença

Este projeto é distribuído sob a [Licença MIT](LICENSE), permitindo o uso, modificação e distribuição do código com restrições mínimas.
