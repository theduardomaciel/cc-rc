try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # type: ignore # ver. < 3.0

# Instanciamos o objeto ConfigParser
config = ConfigParser()

# Lemos o arquivo de configuração
config.read("settings.ini")


class Settings:
    def __init__(self):
        self.config = config

    def __getattr__(self, name):
        # Procura em todas as seções para o atributo solicitado
        for section in self.config.sections():
            if self.config.has_option(section, name):
                # Tenta retornar o valor no tipo correto
                try:
                    # Tenta como int
                    return self.config.getint(section, name)
                except ValueError:
                    try:
                        # Tenta como float
                        return self.config.getfloat(section, name)
                    except ValueError:
                        try:
                            # Tenta como boolean
                            return self.config.getboolean(section, name)
                        except ValueError:
                            # Retorna como string por padrão
                            return self.config.get(section, name)
        raise AttributeError(f"'Settings' object has no attribute '{name}'")

    def update(self, section, key, value):
        self.config.set(section, key, str(value))
        setattr(self, key, value)
        with open("settings.ini", "w") as configfile:
            self.config.write(configfile)

    def add(self, section, key, value):
        self.config.add_section(section)
        self.config.set(section, key, str(value))
        setattr(self, key, value)
        with open("settings.ini", "w") as configfile:
            self.config.write(configfile)

    def remove(self, section, key):
        self.config.remove_option(section, key)
        delattr(self, key)
        with open("settings.ini", "w") as configfile:
            self.config.write(configfile)

    def save(self):
        with open("settings.ini", "w") as configfile:
            self.config.write(configfile)
