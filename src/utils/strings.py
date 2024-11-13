def format_seconds(ms: int):
    """Função para formatar string de tempo em segundos."""
    seconds = ms // 1000
    return f"{seconds} segundo{'s' if seconds != 1 else ''}"

def format_players_amount(amount: int):
    """Função para formatar string de quantidade de jogadores."""
    return f"{amount} jogador{'es' if amount != 1 else ''}"