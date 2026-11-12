from collections import defaultdict

from memoria import Memoria


#
# Olha os acessos que ainda vão acontecer. Se precisar abrir espaço,
# retira a página que vai demorar mais para ser usada de novo.
# Se alguma nunca mais for usada, ela pode sair primeiro.
#
def otimo(referencias, total_molduras):
    futuros = defaultdict(list)
    #
    # Guarda os acessos futuros de trás para frente. Assim, o próximo
    # acesso fica no fim da lista e pode ser retirado com pop().
    #
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
            #
            # Se a lista da página está vazia, ela não vai ser usada de novo.
            #
            vitima = max(
                residentes,
                key=lambda p: futuros[p][-1] if futuros[p] else sem_proximo_acesso,
            )
            residentes.remove(vitima)
        residentes.add(pagina)
    return faltas


#
# Procura primeiro uma página que não foi usada neste ciclo e não
# precisa ser salva. Entre páginas igualmente usadas, prefere a que
# não precisa ser salva.
#
def nru(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    for pagina, instante, operacao in referencias:
        if memoria.acessar(pagina, instante, operacao) is not None:
            continue

        faltas += 1
        vitima = None
        if len(memoria.molduras) == total_molduras:
            #
            # R vale 2 pontos e M vale 1. Sai a página com menos pontos.
            # Se houver empate, sai a primeira na ordem dos espaços da memória.
            #
            moldura = min(
                memoria.molduras,
                key=lambda m: 2 * m.bit_r(instante, ciclo) + m.modificada,
            )
            vitima = memoria.indices[moldura.pagina]
        memoria.carregar(pagina, instante, operacao, vitima)
    return faltas


#
# Olha os espaços da memória em círculo. Quando precisa abrir espaço,
# retira a primeira página que encontra com a marca R desligada.
#
def relogio(referencias, total_molduras, ciclo):
    memoria = Memoria()
    faltas = 0
    ponteiro = 0
    for pagina, instante, operacao in referencias:
        indice = memoria.acessar(pagina, instante, operacao)
        if indice is not None:
            #
            # Quando a página já está na memória, a próxima busca começa no espaço seguinte.
            #
            ponteiro = (indice + 1) % total_molduras
            continue

        faltas += 1
        if len(memoria.molduras) < total_molduras:
            memoria.carregar(pagina, instante, operacao)
            continue

        #
        # Se R estiver ligado, desliga a marca e dá mais uma chance à página.
        # Se todas estiverem marcadas, uma volta basta para desligar todas as marcas.
        #
        while memoria.molduras[ponteiro].bit_r(instante, ciclo):
            memoria.molduras[ponteiro].referenciada = False
            ponteiro = (ponteiro + 1) % total_molduras
        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas


#
# Olha os espaços em círculo à procura de uma página que está há
# bastante tempo sem ser usada e que pode sair sem precisar ser salva.
#
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

        #
        # Uma página é considerada antiga quando o tempo desde o último acesso
        # é maior que o ciclo informado no arquivo.
        #
        for _ in range(total_molduras):
            moldura = memoria.molduras[ponteiro]
            if moldura.bit_r(instante, ciclo):
                moldura.referenciada = False
            elif instante - moldura.ultimo_acesso > ciclo:
                if not moldura.modificada:
                    break
                #
                # Simula salvar a página alterada e segue procurando uma que já esteja salva.
                #
                moldura.modificada = False
            ponteiro = (ponteiro + 1) % total_molduras

        #
        # Se der uma volta inteira sem encontrar a página que queria,
        # retira a que estava no espaço onde a busca começou.
        #
        memoria.carregar(pagina, instante, operacao, ponteiro)
        ponteiro = (ponteiro + 1) % total_molduras
    return faltas
