from calculadora import Processo, resultadoFinal

def fifo(processosOriginais):
    processos = [Processo(pontoAtual.chegada, pontoAtual.duracao) for pontoAtual in processosOriginais]
    processos.sort(key=lambda pontoAtual: pontoAtual.chegada)
    
    tempoAtual = 0
    for pontoAtual in processos:
        if tempoAtual < pontoAtual.chegada:
            tempoAtual = pontoAtual.chegada
            
        pontoAtual.tempoResposta = tempoAtual - pontoAtual.chegada
        tempoAtual += pontoAtual.duracao
        
        pontoAtual.tempoTurnaround = tempoAtual - pontoAtual.chegada
        pontoAtual.tempoEspera = pontoAtual.tempoTurnaround - pontoAtual.duracao
        
    return resultadoFinal(processos)

def sjf(processosOriginais):
    processos = [Processo(pontoAtual.chegada, pontoAtual.duracao) for pontoAtual in processosOriginais]
    processos.sort(key=lambda pontoAtual: pontoAtual.chegada)
    
    tempoAtual = 0
    concluidos = 0
    tamanhoFila = len(processos)
    prontos = []
    i = 0
    
    while concluidos < tamanhoFila:
        while i < tamanhoFila and processos[i].chegada <= tempoAtual:
            prontos.append(processos[i])
            i += 1
            
        if not prontos:
            tempoAtual = processos[i].chegada
            continue
            
        prontos.sort(key=lambda pontoAtual: (pontoAtual.duracao, pontoAtual.chegada))
        pontoAtual = prontos.pop(0)
        
        pontoAtual.tempoResposta = tempoAtual - pontoAtual.chegada
        tempoAtual += pontoAtual.duracao
        
        pontoAtual.tempoTurnaround = tempoAtual - pontoAtual.chegada
        pontoAtual.tempoEspera = pontoAtual.tempoTurnaround - pontoAtual.duracao
        concluidos += 1
        
    return resultadoFinal(processos)

def srt(processosOriginais):
    processos = [Processo(pontoAtual.chegada, pontoAtual.duracao) for pontoAtual in processosOriginais]
    processos.sort(key=lambda pontoAtual: pontoAtual.chegada)
    
    tempoAtual = 0
    concluidos = 0
    tamanhoFila = len(processos)
    prontos = []
    i = 0
    
    while concluidos < tamanhoFila:
        while i < tamanhoFila and processos[i].chegada <= tempoAtual:
            prontos.append(processos[i])
            i += 1
            
        if not prontos:
            tempoAtual = processos[i].chegada
            continue
            
        prontos.sort(key=lambda pontoAtual: (pontoAtual.restante, pontoAtual.chegada))
        pontoAtual = prontos[0]
        
        if pontoAtual.tempoResposta == -1:
            pontoAtual.tempoResposta = tempoAtual - pontoAtual.chegada
            
        pontoAtual.restante -= 1
        tempoAtual += 1
        
        if pontoAtual.restante == 0:
            pontoAtual.concluido = True
            pontoAtual.tempoTurnaround = tempoAtual - pontoAtual.chegada
            pontoAtual.tempoEspera = pontoAtual.tempoTurnaround - pontoAtual.duracao
            prontos.pop(0)
            concluidos += 1
            
    return resultadoFinal(processos)

def rr(processosOriginais, quantum):
    processos = [Processo(pontoAtual.chegada, pontoAtual.duracao) for pontoAtual in processosOriginais]
    processos.sort(key=lambda pontoAtual: pontoAtual.chegada)
    
    tempoAtual = 0
    concluidos = 0
    tamanhoFila = len(processos)
    fila = []
    i = 0
    
    while concluidos < tamanhoFila:
        while i < tamanhoFila and processos[i].chegada <= tempoAtual:
            fila.append(processos[i])
            i += 1
            
        if not fila:
            tempoAtual = processos[i].chegada
            continue
            
        pontoAtual = fila.pop(0)
        
        if pontoAtual.tempoResposta == -1:
            pontoAtual.tempoResposta = tempoAtual - pontoAtual.chegada
            
        tempoExecucao = min(pontoAtual.restante, quantum)
        novoTempo = tempoAtual + tempoExecucao
        
        while i < tamanhoFila and processos[i].chegada <= novoTempo:
            fila.append(processos[i])
            i += 1
            
        tempoAtual = novoTempo
        pontoAtual.restante -= tempoExecucao
        
        if pontoAtual.restante == 0:
            pontoAtual.tempoTurnaround = tempoAtual - pontoAtual.chegada
            pontoAtual.tempoEspera = pontoAtual.tempoTurnaround - pontoAtual.duracao
            concluidos += 1
        else:
            fila.append(pontoAtual)
            
    return resultadoFinal(processos)