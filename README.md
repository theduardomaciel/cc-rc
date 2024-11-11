# Dash Muse

<picture>
  <img alt="Dash Muse" src="/.github/cover.png">
</picture>

**Dash Muse** é um jogo dinâmico multiplayer, desenvolvido em Python, onde os jogadores competem para se tornar o último sobrevivente em uma arena baseada em física e colisões.  
O jogo envolve habilidades de estratégia e reflexo, permitindo que os jogadores promovam ou evitem colisões enquanto permanecem dentro de uma área restrita.

## 🕹️ Sobre

No **Dash Muse**, o objetivo é empurrar outros jogadores para fora da área de jogo, causando-lhes dano.  
Os jogadores começam com 10 vidas (valor configurável) e podem realizar um dash (impulso) a cada 0,5s (500ms) para aumentar as chances de empurrar os inimigos.  

### Interfaces do Jogo

- **Menu Inicial:** Tela de boas-vindas.
- **Sala de Espera:** Espera por pelo menos um jogador para iniciar a partida.
- **Tela de Partida:** Arena onde ocorre o confronto até restar um jogador.

## 🛠 Tecnologias Utilizadas

- **Python:** Linguagem principal do desenvolvimento, desde a lógica do jogo até a manutenção do servidor.
- **Pygame:** Biblioteca para renderização gráfica e manipulação da interface, permitindo atualizações em tempo real dos jogadores.
- **Socket:** Utilizada para configurar a conexão cliente-servidor, possibilitando o multiplayer em rede local.
- **Pickle:** Gerenciamento de objetos serializados para envio dos dados dos jogadores.
- **Threading:** Gerencia as conexões, monitorando eventos e mantendo a comunicação entre cliente e servidor.

## 📂 Estrutura do Código

- **settings.ini:** Configurações do jogo, incluindo tela, regras e rede.
- **requirements.txt:** Lista das bibliotecas necessárias.
- **src/classes:** Classes de componentes da interface e lógica do jogo.
- **src/utils:** Funções auxiliares para renderização e formatação.
- **src/network.py:** Configurações de rede e dados de conexão.
- **src/client.py:** Interface do jogo e gerenciamento dos sprites e eventos.
- **src/server.py:** Configuração do servidor que gerencia as partidas e conexão dos jogadores.

## 🚀 Como executar

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

> [!NOTE]

## 📄 Licença

Este projeto é distribuído sob a [Licença MIT](LICENSE), permitindo o uso, modificação e distribuição do código com restrições mínimas.