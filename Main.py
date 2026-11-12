import os
from paginacao import otimo, nru, relogio, wsclock

def ler_entrada(caminho):
    with open(caminho, encoding="utf-8-sig") as arquivo:
        try:
            total_paginas = int(arquivo.readline())
            total_molduras = int(arquivo.readline())
            ciclo = int(arquivo.readline())
        except ValueError:
            raise ValueError("as três primeiras linhas devem conter inteiros") from None

        if not (1 <= total_paginas <= 2**32 and 1 <= total_molduras <= 2**32):
            raise ValueError("páginas e molduras devem estar entre 1 e 2³²")
        if not 1 <= ciclo <= 1000:
            raise ValueError("o ciclo de R deve estar entre 1 e 1000")

        referencias = []
        for numero, linha in enumerate(arquivo, start=4):
            if not linha.strip():
                continue
            try:
                pagina, instante, operacao = linha.split()
                pagina, instante = map(int, (pagina, instante))
            except ValueError:
                raise ValueError(f"linha {numero}: esperado página, instante e R ou W") from None

            if not 0 <= pagina < total_paginas:
                raise ValueError(f"linha {numero}: página fora do espaço virtual")
            if not 0 <= instante <= 999999 or operacao not in ("R", "W"):
                raise ValueError(f"linha {numero}: instante ou operação inválida")

            referencias.append((pagina, instante, operacao))
    return total_molduras, ciclo, referencias


def main():
    print("Informe o caminho da pasta com os arquivos de teste:")
    caminho = input().strip().strip('"').strip("'")

    for num_teste in range(1, 11):
        nome_teste = f"TESTE-{num_teste:02d}"
        caminho_entrada = os.path.join(caminho, f"{nome_teste}.txt")
        caminho_saida = os.path.join(caminho, f"{nome_teste}-RESULTADO.txt")

        if not os.path.exists(caminho_entrada):
            continue

        try:
            total_molduras, ciclo, referencias = ler_entrada(caminho_entrada)
            resultado_otimo = otimo(referencias, total_molduras)
            resultado_nru = nru(referencias, total_molduras, ciclo)
            resultado_relogio = relogio(referencias, total_molduras, ciclo)
            resultado_wsclock = wsclock(referencias, total_molduras, ciclo)


            with open(caminho_saida, "w", encoding="utf-8") as arquivo:
                arquivo.write(f"{resultado_otimo}\n")
                arquivo.write(f"{resultado_nru}\n")
                arquivo.write(f"{resultado_relogio}\n")
                arquivo.write(f"{resultado_wsclock}\n")
        except (OSError, ValueError) as erro:
            print(f"{nome_teste}: {erro}")
            continue

        print(caminho_saida)

if __name__ == "__main__":
    main()