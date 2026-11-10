from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass
class Moldura:
    pagina: int
    ultimo_acesso: int
    modificada: bool = False
    referenciada: bool = True

    def registrar_acesso(self, instante, operacao):
        self.ultimo_acesso = instante
        self.referenciada = True
        # Uma leitura posterior não desfaz uma escrita ainda não salva.
        if operacao == "W":
            self.modificada = True

    def bit_r(self, instante, ciclo):
        # A mudança de ciclo equivale a zerar R antes do primeiro acesso
        # do novo intervalo, sem percorrer todas as molduras a cada acesso.
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
        moldura = Moldura(pagina, instante, modificada=operacao == "W")
        if indice is None:
            indice = len(self.molduras)
            self.molduras.append(moldura)
        else:
            del self.indices[self.molduras[indice].pagina]
            self.molduras[indice] = moldura
        self.indices[pagina] = indice


def otimo(referencias, total_molduras):
    futuros = defaultdict(deque)
    for posicao, (pagina, _, _) in enumerate(referencias):
        futuros[pagina].append(posicao)

    residentes = set()
    faltas = 0
    sem_proximo_acesso = len(referencias)
    for pagina, _, _ in referencias:
        futuros[pagina].popleft()
        if pagina in residentes:
            continue

        faltas += 1
        if len(residentes) == total_molduras:
            # A primeira posição de cada fila é o próximo uso da página.
            # Uma página que nunca mais será usada tem prioridade para sair.
            vitima = max(
                residentes,
                key=lambda p: futuros[p][0] if futuros[p] else sem_proximo_acesso,
            )
            residentes.remove(vitima)
        residentes.add(pagina)
    return faltas


def nru(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    for pagina, instante, operacao in referencias:
        if memoria.acessar(pagina, instante, operacao) is not None:
            continue

        faltas += 1
        vitima = None
        if len(memoria.molduras) == total_molduras:
            # R tem peso 2 e M tem peso 1, formando as classes 0, 1, 2 e 3.
            # No empate, fica a primeira moldura dessa classe na ordem física.
            vitima = min(
                range(total_molduras),
                key=lambda i: (
                    2 * memoria.molduras[i].bit_r(instante, ciclo)
                    + memoria.molduras[i].modificada
                ),
            )
        memoria.carregar(pagina, instante, operacao, vitima)
    return faltas


def relogio(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    ponteiro = 0
    for pagina, instante, operacao in referencias:
        indice = memoria.acessar(pagina, instante, operacao)
        if indice is not None:
            # Nesta variante, a próxima busca parte da moldura após o acerto.
            ponteiro = (indice + 1) % total_molduras
            continue

        faltas += 1
        if len(memoria.molduras) < total_molduras:
            memoria.carregar(pagina, instante, operacao)
            continue

        # R ligado dá uma segunda chance. Se todos estiverem ligados,
        # uma volta completa os limpa e garante que a busca termine.
        while memoria.molduras[ponteiro].bit_r(instante, ciclo):
            memoria.molduras[ponteiro].referenciada = False
            ponteiro = (ponteiro + 1) % total_molduras
        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas


def wsclock(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    ponteiro = 0
    for pagina, instante, operacao in referencias:
        if memoria.acessar(pagina, instante, operacao) is not None:
            continue

        faltas += 1
        if len(memoria.molduras) < total_molduras:
            memoria.carregar(pagina, instante, operacao)
            continue

        # O enunciado não fornece um limite de idade separado. Usamos
        # o ciclo de R e a idade real desde o último acesso à página.
        for _ in range(total_molduras):
            moldura = memoria.molduras[ponteiro]
            if moldura.bit_r(instante, ciclo):
                moldura.referenciada = False
            elif instante - moldura.ultimo_acesso > ciclo:
                if not moldura.modificada:
                    break
                # Simula a gravação de uma página antiga e suja antes
                # de continuar procurando uma vítima já limpa.
                moldura.modificada = False
            ponteiro = (ponteiro + 1) % total_molduras

        # Se nenhuma vítima ideal apareceu, a volta completa traz o ponteiro
        # de volta ao início. Retiramos essa moldura para garantir progresso.
        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas
