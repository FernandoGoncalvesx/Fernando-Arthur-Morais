class Processo:
    def __init__(self, c, d):
        self.chegada = c
        self.duracao = d
        self.restante = d
        
        self.tempoResposta = -1 
        self.tempoEspera = 0
        self.tempoTurnaround = 0
        self.concluido = False

def resultadoFinal(processos):
    n = len(processos) 
    
    tr = sum(p.tempoResposta for p in processos) / n
    te = sum(p.tempoEspera for p in processos) / n
    tt = sum(p.tempoTurnaround for p in processos) / n
    
    return f"{tr:.3f} {te:.3f} {tt:.3f}".replace(".", ",")