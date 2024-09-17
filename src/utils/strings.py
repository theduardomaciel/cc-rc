def format_seconds(ms: int):
    """Função para formatar string de tempo em segundos."""
    seconds = ms // 1000
    return f"{seconds:02d} segundo{'s' if seconds != 1 else ''}"
