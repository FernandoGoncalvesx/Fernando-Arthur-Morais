from calculadora import Processo, obter_resultado_final

def fifo(processos_originais):
    processos = [Processo(p.chegada, p.duracao) for p in processos_originais]
    processos.sort(key=lambda x: x.chegada)
    
    tempo_atual = 0
    for p_atual in processos:
        if tempo_atual < p_atual.chegada:
            tempo_atual = p_atual.chegada
            
        p_atual.tempo_resposta = tempo_atual - p_atual.chegada
        tempo_atual += p_atual.duracao
        
        p_atual.tempo_turnaround = tempo_atual - p_atual.chegada
        p_atual.tempo_espera = p_atual.tempo_turnaround - p_atual.duracao
        
    return obter_resultado_final(processos)

def sjf(processos_originais):
    processos = [Processo(p.chegada, p.duracao) for p in processos_originais]
    processos.sort(key=lambda x: x.chegada)
    
    tempo_atual = 0
    concluidos = 0
    n = len(processos)
    prontos = []
    i = 0
    
    while concluidos < n:
        while i < n and processos[i].chegada <= tempo_atual:
            prontos.append(processos[i])
            i += 1
            
        if not prontos:
            tempo_atual = processos[i].chegada
            continue
            
        prontos.sort(key=lambda x: (x.duracao, x.chegada))
        p_atual = prontos.pop(0)
        
        p_atual.tempo_resposta = tempo_atual - p_atual.chegada
        tempo_atual += p_atual.duracao
        
        p_atual.tempo_turnaround = tempo_atual - p_atual.chegada
        p_atual.tempo_espera = p_atual.tempo_turnaround - p_atual.duracao
        concluidos += 1
        
    return obter_resultado_final(processos)

def srt(processos_originais):
    processos = [Processo(p.chegada, p.duracao) for p in processos_originais]
    processos.sort(key=lambda x: x.chegada)
    
    tempo_atual = 0
    concluidos = 0
    n = len(processos)
    prontos = []
    i = 0
    
    while concluidos < n:
        while i < n and processos[i].chegada <= tempo_atual:
            prontos.append(processos[i])
            i += 1
            
        if not prontos:
            tempo_atual = processos[i].chegada
            continue
            
        prontos.sort(key=lambda x: (x.restante, x.chegada))
        p_atual = prontos[0]
        
        if p_atual.tempo_resposta == -1:
            p_atual.tempo_resposta = tempo_atual - p_atual.chegada
            
        p_atual.restante -= 1
        tempo_atual += 1
        
        if p_atual.restante == 0:
            p_atual.concluido = True
            p_atual.tempo_turnaround = tempo_atual - p_atual.chegada
            p_atual.tempo_espera = p_atual.tempo_turnaround - p_atual.duracao
            prontos.pop(0)
            concluidos += 1
            
    return obter_resultado_final(processos)

def rr(processos_originais, quantum):
    processos = [Processo(p.chegada, p.duracao) for p in processos_originais]
    processos.sort(key=lambda x: x.chegada)
    
    tempo_atual = 0
    concluidos = 0
    n = len(processos)
    fila = []
    i = 0
    
    while concluidos < n:
        while i < n and processos[i].chegada <= tempo_atual:
            fila.append(processos[i])
            i += 1
            
        if not fila:
            tempo_atual = processos[i].chegada
            continue
            
        p_atual = fila.pop(0)
        
        if p_atual.tempo_resposta == -1:
            p_atual.tempo_resposta = tempo_atual - p_atual.chegada
            
        tempo_execucao = min(p_atual.restante, quantum)
        novo_tempo = tempo_atual + tempo_execucao
        
        while i < n and processos[i].chegada <= novo_tempo:
            fila.append(processos[i])
            i += 1
            
        tempo_atual = novo_tempo
        p_atual.restante -= tempo_execucao
        
        if p_atual.restante == 0:
            p_atual.tempo_turnaround = tempo_atual - p_atual.chegada
            p_atual.tempo_espera = p_atual.tempo_turnaround - p_atual.duracao
            concluidos += 1
        else:
            fila.append(p_atual)
            
    return obter_resultado_final(processos)