from collections import defaultdict
from memoria import Memoria

def otimo(referencias, total_molduras):
    futuros = defaultdict(list)
    for posicao in reversed(range(len(referencias))):
        pagina, _, _ = referencias[posicao]
        futuros[pagina].append(posicao)

    residentes = set()
    faltas = 0
    sem_proximo_acesso = len(referencias)
    for pagina, _, _ in referencias:
        futuros[pagina].pop()
        if pagina in residentes:
            continue

        faltas += 1
        if len(residentes) == total_molduras:
            vitima = max(
                residentes,
                key=lambda p: futuros[p][-1] if futuros[p] else sem_proximo_acesso,
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
            moldura = min(
                memoria.molduras,
                key=lambda m: 2 * m.bit_r(instante, ciclo) + m.modificada,
            )
            vitima = memoria.indices[moldura.pagina]
        memoria.carregar(pagina, instante, operacao, vitima)
    return faltas

def relogio(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    ponteiro = 0
    for pagina, instante, operacao in referencias:
        indice = memoria.acessar(pagina, instante, operacao)
        if indice is not None:
            ponteiro = (indice + 1) % total_molduras
            continue

        faltas += 1
        if len(memoria.molduras) < total_molduras:
            memoria.carregar(pagina, instante, operacao)
            continue

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

        for _ in range(total_molduras):
            moldura = memoria.molduras[ponteiro]
            if moldura.bit_r(instante, ciclo):
                moldura.referenciada = False
            elif instante - moldura.ultimo_acesso > ciclo:
                if not moldura.modificada:
                    break

                moldura.modificada = False
            ponteiro = (ponteiro + 1) % total_molduras

        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas