class Processo:
    def __init__(self, c, d):
        self.chegada = c
        self.duracao = d
        self.restante = d
        
        self.tempo_resposta = -1 
        self.tempo_espera = 0
        self.tempo_turnaround = 0
        self.concluido = False

def obter_resultado_final(processos):
    n = len(processos) 
    
    tr = sum(p.tempo_resposta for p in processos) / n
    te = sum(p.tempo_espera for p in processos) / n
    tt = sum(p.tempo_turnaround for p in processos) / n
    
    return f"{tr:.3f} {te:.3f} {tt:.3f}".replace(".", ",")