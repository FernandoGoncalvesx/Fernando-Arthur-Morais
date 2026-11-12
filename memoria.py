class Moldura:
    def __init__(self, pagina, instante, operacao):
        self.pagina = pagina
        self.ultimo_acesso = instante
        self.modificada = operacao == "W"
        self.referenciada = True

    def registrar_acesso(self, instante, operacao):
        self.ultimo_acesso = instante
        self.referenciada = True
        if operacao == "W":
            self.modificada = True

    def bit_r(self, instante, ciclo):

        return self.referenciada and self.ultimo_acesso // ciclo == instante // ciclo

class Memoria:
    def __init__(self):
        self.molduras = []
        self.indices = {}

    def acessar(self, pagina, instante, operacao):
        indice = self.indices.get(pagina)
        if indice is not None:
            self.molduras[indice].registrar_acesso(instante, operacao)
        return indice

    def carregar(self, pagina, instante, operacao, indice=None):
        moldura = Moldura(pagina, instante, operacao)
        if indice is None:
            indice = len(self.molduras)
            self.molduras.append(moldura)
        else:
            del self.indices[self.molduras[indice].pagina]
            self.molduras[indice] = moldura
        self.indices[pagina] = indice