# Moldura: espaço da memória com uma página + bits R e M
class Moldura:
    # Página entra: R ligado, M ligado se for escrita
    def __init__(self, pagina, instante, operacao):
        self.pagina = pagina
        self.ultimo_acesso = instante
        self.modificada = operacao == "W"
        self.referenciada = True

    # Acerto: atualiza instante, liga R (e M se for escrita)
    def registrar_acesso(self, instante, operacao):
        self.ultimo_acesso = instante
        self.referenciada = True
        if operacao == "W":
            self.modificada = True

    # R só vale se o último acesso foi no ciclo atual
    def bit_r(self, instante, ciclo):
        return self.referenciada and self.ultimo_acesso // ciclo == instante // ciclo


# Memoria: lista de molduras + tabela página -> posição
class Memoria:
    def __init__(self):
        self.molduras = []
        self.indices = {}

    # Acerto: devolve a posição | Falta: devolve None
    def acessar(self, pagina, instante, operacao):
        indice = self.indices.get(pagina)
        if indice is not None:
            self.molduras[indice].registrar_acesso(instante, operacao)
        return indice

    # Carrega a página: em espaço livre ou no lugar da vítima
    def carregar(self, pagina, instante, operacao, indice=None):
        moldura = Moldura(pagina, instante, operacao)
        if indice is None:
            # Espaço livre
            indice = len(self.molduras)
            self.molduras.append(moldura)
        else:
            # Substituição
            del self.indices[self.molduras[indice].pagina]
            self.molduras[indice] = moldura
        self.indices[pagina] = indice
