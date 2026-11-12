from collections import defaultdict

from memoria import Memoria


# ÓTIMO: sai a página que vai demorar mais para ser usada de novo
def otimo(referencias, total_molduras):
    # Próximos acessos de cada página (o próximo fica no fim da lista)
    futuros = defaultdict(list)
    for posicao in reversed(range(len(referencias))):
        pagina, _, _ = referencias[posicao]
        futuros[pagina].append(posicao)

    residentes = set()
    faltas = 0
    sem_proximo_acesso = len(referencias)
    for pagina, _, _ in referencias:
        futuros[pagina].pop()
        # Acerto
        if pagina in residentes:
            continue

        # Falta
        faltas += 1
        # Memória cheia: sai a de uso mais distante
        if len(residentes) == total_molduras:
            vitima = max(
                residentes,
                key=lambda p: futuros[p][-1] if futuros[p] else sem_proximo_acesso,
            )
            residentes.remove(vitima)
        residentes.add(pagina)
    return faltas


# NRU: sai a página da menor classe (2*R + M)
def nru(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    for pagina, instante, operacao in referencias:
        # Acerto
        if memoria.acessar(pagina, instante, operacao) is not None:
            continue

        # Falta
        faltas += 1
        vitima = None
        # Memória cheia: escolhe a menor classe
        if len(memoria.molduras) == total_molduras:
            moldura = min(
                memoria.molduras,
                key=lambda m: 2 * m.bit_r(instante, ciclo) + m.modificada,
            )
            vitima = memoria.indices[moldura.pagina]
        memoria.carregar(pagina, instante, operacao, vitima)
    return faltas


# RELÓGIO: ponteiro em círculo; R=1 ganha segunda chance, R=0 sai
def relogio(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    ponteiro = 0
    for pagina, instante, operacao in referencias:
        indice = memoria.acessar(pagina, instante, operacao)
        # Acerto: ponteiro vai para a moldura seguinte
        if indice is not None:
            ponteiro = (indice + 1) % total_molduras
            continue

        # Falta
        faltas += 1
        # Espaço livre
        if len(memoria.molduras) < total_molduras:
            memoria.carregar(pagina, instante, operacao)
            continue

        # Segunda chance: desliga R e avança
        while memoria.molduras[ponteiro].bit_r(instante, ciclo):
            memoria.molduras[ponteiro].referenciada = False
            ponteiro = (ponteiro + 1) % total_molduras
        # Achou R=0: substitui
        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas


# WSCLOCK: sai a primeira página com R=0, velha (idade > ciclo) e limpa (M=0)
def wsclock(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    ponteiro = 0
    for pagina, instante, operacao in referencias:
        # Acerto: ponteiro não se move
        if memoria.acessar(pagina, instante, operacao) is not None:
            continue

        # Falta
        faltas += 1
        # Espaço livre
        if len(memoria.molduras) < total_molduras:
            memoria.carregar(pagina, instante, operacao)
            continue

        # Uma volta no círculo procurando a vítima
        for _ in range(total_molduras):
            moldura = memoria.molduras[ponteiro]
            # R=1: desliga R
            if moldura.bit_r(instante, ciclo):
                moldura.referenciada = False
            # R=0 e velha
            elif instante - moldura.ultimo_acesso > ciclo:
                # Limpa: é a vítima
                if not moldura.modificada:
                    break
                # Suja: simula gravar no disco
                moldura.modificada = False
            ponteiro = (ponteiro + 1) % total_molduras

        # Substitui (se não achou, sai a do início da volta)
        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas
