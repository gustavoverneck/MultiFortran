import os
import subprocess
import numpy as np
from multiprocessing import Pool

"""
DEFINIÇÃO DOS VALORES DE ENTRADA
"""

# numero = j * 10^e
e0 = 0      # Exponente inicial
e1 = 15     # Exponente final
j0 = 1      # Escalar inicial
j1 = 9      # Escalar final

parametros = []
for j in range(j0, j1, 1):
    for e in range(e0, e1, 1):
        parametros.append(f"{j}.0d{e}")
parametros = np.array(parametros)


num_processos = int(8)       # Escolher de acordo com o número de núcleos do processador e a capacidade de memória
nome_executavel = "template.o"  # Nome do executável gerado pelo compilador
nome_template = "template.f"    # Nome do arquivo de template
input_dir = "input"             # Nome da pasta de entrada


# ------------------------------------------------------------------------------------------------------------------
# Cria arquivo para armazenar os parâmetros
if not os.path.exists("output/params.txt"):
        with open("output/params.txt", "w") as f:
            f.write("Parametros:\n")
else:
    with open("output/params.txt", "w") as f:
        f.write("Parametros:\n")

# ------------------------------------------------------------------------------------------------------------------
def getstr(param):
    """
    Função que converte um número em string, com 4 casas decimais.
    """
    return "{:.20f}".format(param)
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
def compile_template(param):
    """
    Função que compila o programa Fortran.
    """
    os.system("gfortran -w " + f"output/{param}/template.f -o " + f"output/{param}/{param}"+".o")

# ------------------------------------------------------------------------------------------------------------------
def compile_tov(param):
    """
    Função que compila o programa Fortran.
    """
    os.system("gfortran -w " + f"output/{param}/tov.f -o " + f"output/{param}/tov.o")

# ------------------------------------------------------------------------------------------------------------------
def move_ex(param):
    """
    Função que copia o executável para a pasta específica.
    """
    global nome_executavel, nome_template
    os.system(f"cp {input_dir}/{nome_template} output/{param}/{nome_template}")
    os.system(f"cp {input_dir}/tov.f output/{param}/tov.f")
    compile_template(param)
    compile_tov(param)

# ------------------------------------------------------------------------------------------------------------------
def fixEndOfFile(param):
    """
    Função que corrige o final do arquivo de saída.
    """    
    # Adiciona "-1. -1. -1, -1" ao fim de cada eos.dat dentro da pasta output/params
    eos_file_path = f"output/{param}/eos.dat"
    if os.path.exists(eos_file_path):
        with open(eos_file_path, "a") as eos_file:
            eos_file.write("\n-1. -1. -1 -1\n")
# ------------------------------------------------------------------------------------------------------------------
def exportParams(param):
    """
    Função que exporta os parâmetros para o arquivo de entrada.
    """
    with open(f"output/params.txt", "a") as f:
        f.write(f"{param}\n")

# ------------------------------------------------------------------------------------------------------------------
def execute(param):
    """
    Função que executa o programa Fortran com um parâmetro específico.
    """
    print(f"Executando com parâmetro {param}")
    exportParams(param)
    create_folder(param)
    move_ex(param)
    executable = f"./{param}.o"
    # Executa o programa com o parâmetro específico
    subprocess.run([executable, param], capture_output=False, text=True, cwd=f"output/{param}")
    fixEndOfFile(param)
    # Executa tov
    subprocess.run(["./tov.o"], capture_output=False, text=True, cwd=f"output/{param}")

    pass
# ------------------------------------------------------------------------------------------------------------------
def main():
    global num_processos, current_process, parametros
    
    setup()

    # Usa multiprocessing.Pool para paralelizar
    with Pool(num_processos) as pool:
        pool.map(execute, parametros)
        
    print("Execução finalizada.")

# ------------------------------------------------------------------------------------------------------------------
# Executa a função main se este script for executado diretamente
if __name__ == "__main__":
    main()
