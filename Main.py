import os
from calculadora import Processo
from escalonadores import fifo, sjf, srt, rr

def main():
    print("Jogue o caminho:")
    caminhoJogar = input()
    caminho = caminhoJogar.strip().strip('"').strip("'")
    
    for num_teste in range(1, 11):
        arquivoEntrada = f"TESTE-{num_teste:02d}.txt"
        caminhoEntrada = os.path.join(caminho, arquivoEntrada)
        
        if not os.path.exists(caminhoEntrada):
            continue
            
        with open(caminhoEntrada, 'r') as f:
            linhas = f.readlines()
            
        if len(linhas) == 0:
            print(f"O arquivo {arquivoEntrada} vazio")
            continue
            
        quantum = int(linhas[0].strip())
        processos = []
        
        for linha in linhas[1:]:
            if linha.strip():
                c, d = map(int, linha.strip().split())
                processos.append(Processo(c, d))
                
        resultadoFifo = fifo(processos)
        resultadoSjf = sjf(processos)
        resultadoSrt = srt(processos)
        resultadoRr = rr(processos, quantum)
        
        ArquivoSaida = f"TESTE-{num_teste:02d}-RESULTADO.txt"
        caminho_completo_saida = os.path.join(caminho, ArquivoSaida)
        
        with open(caminho_completo_saida, 'w') as f:
            f.write(resultadoFifo + "\n")
            f.write(resultadoSjf + "\n")
            f.write(resultadoSrt + "\n")
            f.write(resultadoRr + "\n")
            
        print(f"{caminho_completo_saida}")

if __name__ == "__main__":
    main()