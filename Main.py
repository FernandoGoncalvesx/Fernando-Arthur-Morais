import os

from calculadora import Processo
from escalonadores import fifo, sjf, srt, rr

def main():
    print("Jogue o caminho da pasta:")
    caminhoJogar = input()
    caminho_pendrive = caminhoJogar.strip()
    
    for num_teste in range(1, 11):
        nome_arquivo_entrada = f"TESTE-{num_teste:02d}.txt"
        
        caminho_completo_entrada = os.path.join(caminho_pendrive, nome_arquivo_entrada)
        
        if not os.path.exists(caminho_completo_entrada):
            continue
            
        with open(caminho_completo_entrada, 'r') as f:
            linhas = f.readlines()
            
        if len(linhas) == 0:
            print(f"O arquivo {nome_arquivo_entrada} vazio")
            continue
            
        quantum = int(linhas[0].strip())
        processos = []
        
        for idx, linha in enumerate(linhas[1:]):
            if linha.strip():
                chegada, duracao = map(int, linha.strip().split())
                processos.append(Processo(idx, chegada, duracao))
                
        resultado_fifo = fifo(processos)
        resultado_sjf = sjf(processos)
        resultado_srt = srt(processos)
        resultado_rr = rr(processos, quantum)
        
        nome_arquivo_saida = f"TESTE-{num_teste:02d}-RESULTADO.txt"
        
        caminho_completo_saida = os.path.join(caminho_pendrive, nome_arquivo_saida)
        
        with open(caminho_completo_saida, 'w') as f:
            f.write(resultado_fifo + "\n")
            f.write(resultado_sjf + "\n")
            f.write(resultado_srt + "\n")
            f.write(resultado_rr + "\n")
            
        print(f"{caminho_completo_saida}")

if __name__ == "__main__":
    main()