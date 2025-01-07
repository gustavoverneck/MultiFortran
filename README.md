# MultiFortran
Um script em Python para rodar um template de fortran em paralelo utilizando múltiplos parâmetros.

## Tutorial de utilização do programa

###  Criação do template em Fortran:
    
    O primeiro passo para a utilização do código é a criação de um arquivo
    template em F90 que receba o parâmetro via linha de comando, do seguinte modo:

    - Declaração de variável

    """
    REAL :: CSI                               # Define uma variável real
    character(len=32) :: csi_string           # Variável de caractere para capturar o argumento
    integer :: iostat                         # Variável para verificar se a leitura foi bem sucedida
    call get_command_argument(1, csi_string)  # Obtém o argumento da linha de comando
    read(csi_string, *, iostat=iostat) csi    # Converte o argumento de string para real
    """
