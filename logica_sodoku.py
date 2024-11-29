import random
import copy

def es_valido(tablero:list, fila:int, col:int, num:int):
    """
    Verifica si un número puede colocarse en una posición específica del tablero de Sudoku

    Recibe:
        tablero: La matriz 9x9 que representa el tablero de Sudoku
        fila: El índice de la fila donde se quiere colocar el número
        col: El índice de la columna donde se quiere colocar el número
        num: El número que se quiere verificar

    Retorno:
        True si el número puede colocarse en la posición (fila, col) sin violar las reglas
        False si el número ya está presente en la fila, la columna o el bloque 3x3 correspondiente
    """
    
    # Inicializa la bandera como True.
    bandera_retorno = True #(el número no está repetido en la fila, columna o bloque)

    # Verifica si el numero ya está en la fila
    if num in tablero[fila]:
        bandera_retorno = False
    
    # Verifica si el numero ya está en la columna
    for i in range(9):
        if tablero[i][col] == num:
            bandera_retorno = False
    
    # Verifica si el número ya está en el bloque 3x3 correspondiente
    # Determina la fila y la columna inicial del bloque 3x3 al que pertenece la celda
    bloque_fila = (fila // 3) * 3
    bloque_col = (col // 3) * 3
    
    # Recorre las celdas del bloque 3x3
    for i in range(bloque_fila, bloque_fila + 3):
        for j in range(bloque_col, bloque_col + 3):
            if tablero[i][j] == num:
                bandera_retorno = False
                break
    
    return bandera_retorno

def inicializar_matriz(cant_filas:int, cant_columnas:int, valor_inicial:any)->list:
    """
    Inicializa una matriz con un valor específico en todas sus celdas.

    Recibe:
        cant_filas: El número de filas de la matriz
        cant_columnas: El número de columnas de la matriz
        valor_inicial: El valor que debe tener cada celda de la matriz

    Retorna:
        Una matriz de dimensiones cant_filas x cant_columnas, llena con valor_inicial
    """
    matriz = []
    for _ in range(cant_filas):
        fila = [valor_inicial] * cant_columnas
        matriz += [fila]
    return matriz


def llenar_tablero(tablero: list[list]) -> bool:
    """
    Llena un tablero de Sudoku usando backtracking, asegurándose de seguir las reglas del Sudoku.
    
    Recibe:
        tablero: Una matriz 9x9 que representa el tablero de Sudoku con celdas vacías (0).
    
    Retorno:
        True si el tablero fue llenado completamente y es válido.
        False si no se pudo llenar el tablero.
    """
    tablero_lleno = True  # Asume que el tablero está lleno
    
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:  # Encuentra una celda vacía
                numeros = list(range(1, 10))
                random.shuffle(numeros)  # Mezcla los números aleatoriamente
                tablero_lleno = False  # Hay al menos una celda vacía, asume que no está lleno      
                
                for num in numeros:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num  # Coloca un número válido
                        
                        if llenar_tablero(tablero):  # Llama recursivamente
                            tablero_lleno = True  # Si encuentra solución, marca como lleno   #Backtraking
                            break
                        
                        tablero[fila][col] = 0  # Retrocede si no encuentra solución
                break  # Sale si no puede colocar un número válido
                
        if not tablero_lleno:
            break  # Sale del bucle externo si no puede llenar el tablero
    
    return tablero_lleno  # Devuelve el estado del tablero


def generar_tablero() -> list[list]:
    """
    Genera un tablero de Sudoku válido, con todos los números colocados siguiendo las reglas.

    Retorno:
        Una matriz 9x9 que representa el tablero de Sudoku completo y resuelto.
        Si no se puede generar un tablero válido, devuelve una matriz vacía.
    """
    tablero = inicializar_matriz(9, 9, 0)  # Inicializa un tablero vacío
    tablero_lleno = llenar_tablero(tablero)
    
    if not tablero_lleno:
        tablero = []
    
    return tablero


    
# Funcion auxiliar que cambia numeros por ceros segun la dificultad
def generar_sudoku(tablero_lleno:list[list], dificultad:str) -> list[list]:
    """
    Elimina números del tablero según la dificultad.
    
    Fácil: 20% de las celdas vacías.
    Medio: 40% de las celdas vacías.
    Difícil: 60% de las celdas vacías.

    Recibe:
    tablero_lleno (list[list]) : Tablero completo sin borrar numeros
    dificultad (str): Recibe la dificultad seleccionada.
    
    Retorna:
    sudoku_final(list[list]): Sudoku con celdas igualadas a 0 para que no se muestren en pantalla.

    """
    
    # Crear una copia profunda del tablero para no modificar el original
    sudoku_final = copy.deepcopy(tablero_lleno) #para que no modifique tablero lleno tambien
    
    if dificultad == "Facil":
        porcentaje = 0.2
    elif dificultad == "Medio":
        porcentaje = 0.4
    elif dificultad == "Dificil":
        porcentaje = 0.6

    celdas_a_eliminar = int(9 * 9 * porcentaje)
    #celdas_a_eliminar = 1
    while celdas_a_eliminar > 0:
        fila = random.randint(0, 8)
        col = random.randint(0, 8)
        if sudoku_final[fila][col] != 0:
            sudoku_final[fila][col] = 0
            celdas_a_eliminar -= 1
    
    return sudoku_final


def generar_matriz_booleana(sudoku:list[list]) -> list[list[bool]]:
    '''
    A partir del sudoku original genera una matriz con valores booleanos donde cada posición tiene False si es 0(cero), True si tiene valor asignado.
    
    Recibe:
        sudoku: matriz generada con la dificultad aplicada
    Devuelve:
        matriz_booleana: matriz con valores booleanos generada a partir de los valores del sudoku
    
    False = 0
    True = 1 - 9
    '''
    matriz_booleana = []
    for fila in sudoku: #recorre el sudoku que tiene 0
        fila_booleana = [] #genera la misma lista pero booleana
        for celda in fila:
            fila_booleana.append(celda != 0) # Coloca true si la celda no es cero, False si es cero
        matriz_booleana.append(fila_booleana)

    return matriz_booleana


def comprobar_igualdad_celda(sudoku, tablero_lleno, fila, col) -> bool:
    '''
    Comprueba sudoku[fila][col] contra tablero_lleno[fila][col] y si los numeros en esas coordenadas son identicos, devuelve True.
    Se utiliza para corroborar que el numero ingresado es correcto
    
    Recibe:
    sudoku (list[list]): Sudoku con 0 incluidos
    tablero_lleno (list[list]): Sudoku sin 0
    fila (int): Fila del sudoku
    col (int): Columna del sudoku
    '''
    bandera_igualdad = False
    if sudoku[fila][col] == tablero_lleno[fila][col] or sudoku[fila][col] == 0:
        bandera_igualdad = True
        
    return bandera_igualdad

