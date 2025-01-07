import os
import subprocess
import numpy as np
from multiprocessing import Pool

"""
DEFINIÇÃO DOS VALORES DE ENTRADA
"""

csi_inicial = 0.1
csi_final = 0.2
n_csi = 100
d_csi = abs((csi_final - csi_inicial) / n_csi)

num_processos = int(8)       # Escolher de acordo com o número de núcleos do processador e a capacidade de memória
nome_executavel = "template.o"  # Nome do executável gerado pelo compilador
nome_template = "template.f"    # Nome do arquivo de template

# ------------------------------------------------------------------------------------------------------------------
def getstr(param):
    """
    Função que converte um número em string, com 4 casas decimais.
    """
    return "{:.3f}".format(param)
# ------------------------------------------------------------------------------------------------------------------
def setup():
    """
    Função que organiza a estrutura de pastas.
    """
    # Exclui a pasta de saída, se existir
    if os.path.exists("output"):
        os.system("rm -r output")
    # Cria a pasta de saída
    if not os.path.exists("output"):
        os.makedirs("output")

# ------------------------------------------------------------------------------------------------------------------
def create_folder(param):
    """
    Função que cria a pasta de saída.
    """
    if not os.path.exists(f"output/{param}"):
        os.makedirs("output/" + (param))

# ------------------------------------------------------------------------------------------------------------------
def compile(param):
    """
    Função que compila o programa Fortran.
    """
    os.system("gfortran -w " + f"output/{param}/template.f -o " + f"output/{param}/{param}"+".o")

# ------------------------------------------------------------------------------------------------------------------
def move_ex(param):
    """
    Função que copia o executável para a pasta específica.
    """
    global nome_executavel, nome_template
    os.system(f"cp {nome_template} output/{param}/{nome_template}")
    compile(param)

# ------------------------------------------------------------------------------------------------------------------
def execute(param):
    """
    Função que executa o programa Fortran com um parâmetro específico.
    """
    print(f"Executando com parâmetro {param}")
    create_folder(getstr(param))
    move_ex(getstr(param))
    executable = f"./{getstr(param)}.o"
    result = subprocess.run([executable, getstr(param)], capture_output=False, text=True, cwd=f"output/{getstr(param)}")
    return result.stdout

# ------------------------------------------------------------------------------------------------------------------
def main():
    global num_processos, current_process
    
    setup()

    # Lista de parâmetros que você quer testar
    parametros = np.arange(csi_inicial, csi_final, d_csi) # (valor_inicial, valor_final, passo)

    # Define o número de processos paralelos (pode ser o número de núcleos da CPU, por exemplo)

    # Usa multiprocessing.Pool para paralelizar
    with Pool(num_processos) as pool:
        pool.map(execute, parametros)
        
    print("Execução finalizada.")

# ------------------------------------------------------------------------------------------------------------------
# Executa a função main se este script for executado diretamente
if __name__ == "__main__":
    main()
