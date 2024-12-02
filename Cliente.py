class Cliente:
    def __init__(self, name, fone):
        self._nome = name
        self._telefone = fone

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome
