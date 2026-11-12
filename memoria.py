#
# Uma moldura é um espaço da memória que guarda uma página.
# R marca que a página foi usada. M marca que ela foi alterada
# e ainda precisa ser salva.
#
class Moldura:
    def __init__(self, pagina, instante, operacao):
        self.pagina = pagina
        self.ultimo_acesso = instante
        self.modificada = operacao == "W"
        self.referenciada = True

    #
    # Anota quando a página foi usada e liga a marca R.
    #
    def registrar_acesso(self, instante, operacao):
        self.ultimo_acesso = instante
        self.referenciada = True
        #
        # Ler uma página não apaga a marca de uma alteração que ainda precisa ser salva.
        #
        if operacao == "W":
            self.modificada = True

    def bit_r(self, instante, ciclo):
        #
        # Se a página foi usada em um ciclo anterior, trata R como desligado.
        # Assim, não é preciso apagar a marca de todas as páginas de uma vez.
        #
        return self.referenciada and self.ultimo_acesso // ciclo == instante // ciclo


#
# Guarda as páginas na ordem dos espaços da memória.
# Também guarda a posição de cada página para encontrá-la rapidamente.
#
class Memoria:
    def __init__(self):
        self.molduras = []
        self.indices = {}

    #
    # Se a página está na memória, anota o acesso e devolve a posição dela.
    # Se não está, devolve None, que aqui significa que a página não foi encontrada.
    #
    def acessar(self, pagina, instante, operacao):
        indice = self.indices.get(pagina)
        if indice is not None:
            self.molduras[indice].registrar_acesso(instante, operacao)
        return indice

    #
    # Se nenhuma posição foi indicada, coloca a página no próximo espaço livre.
    # Se uma posição foi indicada, retira a página antiga e coloca a nova no lugar.
    #
    def carregar(self, pagina, instante, operacao, indice=None):
        moldura = Moldura(pagina, instante, operacao)
        if indice is None:
            indice = len(self.molduras)
            self.molduras.append(moldura)
        else:
            del self.indices[self.molduras[indice].pagina]
            self.molduras[indice] = moldura
        self.indices[pagina] = indice
