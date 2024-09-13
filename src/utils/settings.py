# settings.py
from configparser import ConfigParser

config = ConfigParser()
config.read("settings.ini")


class Settings:
    def __init__(self):
        self.config = config
        self._cache = {}  # Cache para armazenar valores já acessados

    def __getattr__(self, name):
        if name in self._cache:
            return self._cache[name]

        # Verifica se o atributo está em cache
        for section in self.config.sections():
            if self.config.has_option(section, name):
                value = self._get_typed_value(section, name)
                self._cache[name] = value  # Armazena no cache
                return value

        raise AttributeError(f"'Settings' object has no attribute '{name}'")

    # TODO: Otimizar a performance
    def _get_typed_value(self, section, name):
        """Retorna o valor no tipo correto."""
        try:
            return self.config.getint(section, name)
        except ValueError:
            try:
                return self.config.getfloat(section, name)
            except ValueError:
                try:
                    return self.config.getboolean(section, name)
                except ValueError:
                    return self.config.get(section, name)

    def update(self, section, key, value):
        self.config.set(section, key, str(value))
        self._cache[key] = value  # Atualiza o cache
        self._save()

    def add(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self._cache[key] = value  # Atualiza o cache
        self._save()

    def remove(self, section, key):
        if self.config.remove_option(section, key):
            self._cache.pop(key, None)  # Remove do cache
            self._save()

    def _save(self):
        """Salva o arquivo de configuração somente quando houver mudanças."""
        with open("settings.ini", "w") as configfile:
            self.config.write(configfile)
