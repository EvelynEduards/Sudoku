import pygame
from configuraciones import *
from puntaje import *
from logica_sodoku import *

#------------------------------------------------------------------------------------------------------------------------
#FUNCIONES MOVIDAS DEL MAIN A LA BIBLIOTECA
# Función para calcular celdas a resaltar
def calcular_resaltado(fila:int, col:int) -> list:
    '''
    Esta funcion calcula las celdas resaltadas de un tablero basandose en una fila, una columna y un bloque 3x3
    Verifica previamente si la selección está dentro del tablero.
        Recibe:
        fila (int) sería la fila seleccionada del tablero.
        col (int) sería la columna seleccionada del tablero.
        Devuelve:
        celdas_resaltadas (list) una lista con las coordenadas de las celdas resaltadas.
    '''
    # Verificar si la celda seleccionada está dentro del área válida
    if 0 <= fila < 9 and 0 <= col < 9:
        celdas_resaltadas = []

        # Resaltar la fila completa
        for c in range(9):
            celdas_resaltadas.append((fila, c))

        # Resaltar la columna completa
        for f in range(9):
            celdas_resaltadas.append((f, col))

        # Resaltar el bloque 3x3
        bloque_fila = (fila // 3) * 3
        bloque_col = (col // 3) * 3
        for f in range(bloque_fila, bloque_fila + 3):
            for c in range(bloque_col, bloque_col + 3):
                celdas_resaltadas.append((f, c))
    else:
        celdas_resaltadas = []  # Si está fuera del tablero, no hay resaltado
    
    return celdas_resaltadas


def crear_fondo_transparente(TABLERO_ANCHO:int, TABLERO_ALTO:int, BLANCO:tuple) -> pygame.Surface:
    '''
    Crea un fondo semi-transparente para el tablero.

    Esta función crea una superficie de un tamaño determinado (por las dimensiones del tablero) 
    y le aplica un color de fondo con una transparencia establecida. Es útil para colocar 
    sobre el tablero y dar un efecto de fondo transparente.

    Parámetros:
    TABLERO_ANCHO (int): El ancho del tablero.
    TABLERO_ALTO (int): El alto del tablero.
    BLANCO (tuple): El color de fondo en formato RGB (blanco en este caso).

    Devuelve:
    pygame.Surface: Una superficie de Pygame con el fondo semi-transparente para el tablero.
    '''
    # Crea superficie con el tamaño especificado
    fondo_transparente = pygame.Surface((TABLERO_ANCHO, TABLERO_ALTO))
    fondo_transparente.fill(BLANCO) # Rellena la superficie con el color especificado (en este caso, blanco).
    fondo_transparente.set_alpha(220)  # Aplica un nivel de transparencia a la superficie. 
    return fondo_transparente


def dibujar_lineas(ventana: pygame.display, TAMANIO_TABLERO:int, NEGRO:tuple,
                    MARGEN_IZQUIERDO:int, MARGEN_SUPERIOR:int, tamanio_celda:int,
                      TABLERO_ANCHO:int, TABLERO_ALTO:int) -> None:
    '''
    Dibuja las líneas de la cuadrícula en el tablero de juego.

    Esta función dibuja las líneas que forman la cuadrícula del tablero de Sudoku 
    en la ventana proporcionada, utilizando las dimensiones y márgenes especificados.

    Parámetros:
    ventana (pygame.display): La ventana de Pygame donde se dibujarán las líneas de la cuadrícula.
    TAMANIO_TABLERO (int): El tamaño del tablero, generalmente el número de celdas por fila o columna.
    NEGRO (tuple): El color de las líneas en formato RGB (negro).
    MARGEN_IZQUIERDO (int): El margen a la izquierda del tablero.
    MARGEN_SUPERIOR (int): El margen superior del tablero.
    tamanio_celda (int): El tamaño de cada celda del tablero.
    TABLERO_ANCHO (int): El ancho total del tablero, en píxeles.
    TABLERO_ALTO (int): El alto total del tablero, en píxeles.

    Devuelve:
    None: Esta función no devuelve ningún valor.
    '''
    # Este bucle dibuja las líneas horizontales y las verticales
    for i in range(TAMANIO_TABLERO + 1):
        # Si el índice de la línea es múltiplo de 3 (líneas más gruesas para los bloques principales)
        grosor = 4 if i % 3 == 0 else 1
        # Dibuja una línea horizontal:
        pygame.draw.line(ventana, NEGRO, (MARGEN_IZQUIERDO, MARGEN_SUPERIOR + i * tamanio_celda), 
                         (MARGEN_IZQUIERDO + TABLERO_ANCHO, MARGEN_SUPERIOR + i * tamanio_celda), grosor) # Empieza en el margen izquierdo y se extiende horizontalmente según el ancho del tablero.
        # Dibuja una línea vertical:
        pygame.draw.line(ventana, NEGRO, (MARGEN_IZQUIERDO + i * tamanio_celda, MARGEN_SUPERIOR), # Empieza en el margen superior y se extiende verticalmente según el alto del tablero.
                         (MARGEN_IZQUIERDO + i * tamanio_celda, MARGEN_SUPERIOR + TABLERO_ALTO), grosor)


def dibujar_numero(ventana: pygame.display, num: int, fila: int, col: int,
                    matriz_booleana: list[list[bool]], sudoku:list[list[int]],
                      tablero_lleno:list[list[int]], fuente_numeros: pygame.font, NEGRO:tuple,
                        ROJO:tuple, AZUL:tuple, MARGEN_IZQUIERDO:int, MARGEN_SUPERIOR:int, tamanio_celda:int) -> None:
    '''
    Esta función renderiza un número en la celda correspondiente del tablero de Sudoku y lo colorea 
    según si el número fue ingresado por el usuario, si es correcto o incorrecto en relación con la solución del Sudoku.

    Parámetros:
    ventana (pygame.display): La ventana de Pygame donde se dibujará el número.
    num (int): El número que se va a dibujar. Si es 0, no se dibuja nada.
    fila (int): La fila del tablero donde se dibuja el número (índice basado en 0).
    col (int): La columna del tablero donde se dibuja el número (índice basado en 0).
    matriz_booleana (list[list[bool]]): Una matriz que indica si el número fue ingresado por el usuario (True) o es parte del tablero inicial (False).
    sudoku (list[list[int]]): La matriz actual del Sudoku con los números ingresados hasta el momento.
    tablero_lleno (list[list[int]]): La solución completa del Sudoku, utilizada para verificar errores.
    fuente_numeros (pygame.font): La fuente de texto utilizada para renderizar los números.
    NEGRO (tuple): El color negro en formato RGB, utilizado para dibujar números ingresados por el usuario.
    ROJO (tuple): El color rojo en formato RGB, utilizado para dibujar números incorrectos.
    AZUL (tuple): El color azul en formato RGB, utilizado para dibujar números correctos.
    MARGEN_IZQUIERDO (int): El margen izquierdo donde comienza el tablero en la ventana.
    MARGEN_SUPERIOR (int): El margen superior donde comienza el tablero en la ventana.
    tamanio_celda (int): El tamaño de cada celda del tablero.

    Retorno:
    None: Esta función no devuelve ningún valor.
    '''
    if num != 0: # Si el numero es 0 no dibuja nada
        
        if matriz_booleana[fila][col]:  # Si el número fue ingresado 
            color = NEGRO  # Se pinta de negro
        else:
            if not comprobar_igualdad_celda(sudoku, tablero_lleno, fila, col):
                color = ROJO # Si es incorrecto pinta de rojo
            else:
                color = AZUL  # Si es correcto pinta de azul
        # Renderiza el número con la fuente especificada y el color calculado.
        texto = fuente_numeros.render(str(num), True, color)
        
        # Calcula las coordenadas para centrar el texto dentro de la celda correspondiente.
        x = (MARGEN_IZQUIERDO 
             + col * tamanio_celda 
             + tamanio_celda // 2           # Margen izquierdo + n° de columna * tamaño de celda +  tamaño de celda / 2 - ancho del texto / 2
             - texto.get_width() // 2)      # Es decir que lo dibuja en la mitad del espacio sobrante, para que el sobrante quede mitad en la izquierda y mitad en la derecha
        y = (MARGEN_SUPERIOR 
             + fila * tamanio_celda 
             + tamanio_celda // 2 
             - texto.get_height() // 2)
        # Dibuja el numero en la ventana
        ventana.blit(texto, (x, y))
    

def resaltar_celdas(ventana: pygame.display, fila: int, col: int, cantidad:str, sudoku:list[list],
                    tablero_lleno:list[list[int]], CELESTE:tuple, AZUL_CLARO:tuple, GRIS_OSCURO:tuple,
                    ROSA:tuple, ROSA_CLARO:tuple, MARGEN_IZQUIERDO:int, MARGEN_SUPERIOR:int, tamanio_celda:int) -> None:
    '''
    Esta función dibuja un resaltado visual sobre las celdas de la ventana del juego, dependiendo del tipo de 
    resaltado seleccionado: todas las celdas asociadas con la celda seleccionada (como la fila, columna y región 3x3) 
    o solo la celda seleccionada.

    Parámetros:
    ventana (pygame.display): La ventana de Pygame donde se dibujarán las celdas resaltadas.
    fila (int): La fila de la celda seleccionada en el tablero (índice basado en 0).
    col (int): La columna de la celda seleccionada en el tablero (índice basado en 0).
    cantidad (str): Tipo de resaltado que se aplicará. Puede ser:
                    - "todas": Resalta todas las celdas relacionadas (fila, columna, y región 3x3).
                    - "una": Resalta únicamente la celda seleccionada.
    sudoku (list[list[int]]): La matriz que representa el tablero actual del Sudoku con los números ingresados hasta el momento.
    tablero_lleno (list[list[int]]): La matriz que representa la solución completa y correcta del Sudoku.
    CELESTE (tuple): Color en formato RGB para resaltar en celeste.
    AZUL_CLARO (tuple): Color en formato RGB para resaltar en azul claro.
    GRIS_OSCURO (tuple): Color en formato RGB para resaltar en gris oscuro.
    ROSA (tuple): Color en formato RGB para resaltar en rosa.
    ROSA_CLARO (tuple): Color en formato RGB para resaltar en rosa claro.
    MARGEN_IZQUIERDO (int): El margen izquierdo donde comienza el tablero en la ventana.
    MARGEN_SUPERIOR (int): El margen superior donde comienza el tablero en la ventana.
    tamanio_celda (int): El tamaño de cada celda del tablero en píxeles.
    
    Retorno:
    None: Esta función no devuelve ningún valor, realiza las operaciones gráficas directamente sobre la ventana proporcionada.
    '''
    # Calcula las celdas a resaltar dependiendo de la fila, columna y bloque 
    celdas_resaltadas = calcular_resaltado(fila, col)
    # Itera todas las celdas que deben ser resaltadas
    for f, c in celdas_resaltadas:
        # Verifica si la celda resaltada coincide con la solución
        if comprobar_igualdad_celda(sudoku, tablero_lleno, fila, col):
            
            if cantidad == "todas": # Si cantidad = "todas" resalta todo lo correspondiente
                # Dibuja las celdas de color resltado correspondiente
                pygame.draw.rect(ventana, CELESTE, 
                                (MARGEN_IZQUIERDO 
                                  + c * tamanio_celda, MARGEN_SUPERIOR 
                                  + f * tamanio_celda, tamanio_celda, tamanio_celda))
                # Destaca la celda principal seleccionada de otro color
                pygame.draw.rect(ventana, AZUL_CLARO, 
                                (MARGEN_IZQUIERDO 
                                  + col * tamanio_celda, MARGEN_SUPERIOR 
                                  + fila * tamanio_celda, tamanio_celda, tamanio_celda))
            # Esto es para que puedas seleccionar fuera de las permitidas si queres que resalte alguna en particular
            elif cantidad == "una":
                # Resalta las que no se pueden escribir de color gris
                pygame.draw.rect(ventana, GRIS_OSCURO, 
                                (MARGEN_IZQUIERDO 
                                  + col * tamanio_celda, MARGEN_SUPERIOR 
                                  + fila * tamanio_celda, tamanio_celda, tamanio_celda))
                # Con esto resaltaría unicamente la seleccionada
        else:
            # Resalta de otro color cuando el numero no coincide con la solución
            pygame.draw.rect(ventana, ROSA, 
                            (MARGEN_IZQUIERDO 
                              + c * tamanio_celda, MARGEN_SUPERIOR 
                              + f * tamanio_celda, tamanio_celda, tamanio_celda))
            # Destaca la celda seleccionada con otro rosa
            pygame.draw.rect(ventana, ROSA_CLARO, 
                            (MARGEN_IZQUIERDO 
                              + col * tamanio_celda, MARGEN_SUPERIOR 
                              + fila * tamanio_celda, tamanio_celda, tamanio_celda))

def manejar_entrada(fila: int, col: int, sudoku:list[list]) -> int:
    '''
    Captura las teclas presionadas para ingresar o borrar números en el tablero de Sudoku.
    Permite asignar números del 1 al 9 a una celda seleccionada y borrar su contenido.

    Parámetros:
        fila (int): La fila de la celda seleccionada.
        col (int): La columna de la celda seleccionada.
        sudoku (list[list]): La matriz del tablero de Sudoku donde se ingresarán o borrarán los números.

    Retorno:
        resultado(int): El valor de la tecla presionada
        cambio_realizado(bool): Notifica si hubo o no cambios en la celda
    '''
    # Captura el estado de todas las teclas en el teclado
    teclas = pygame.key.get_pressed()
    resultado = -1  # Valor por defecto si no hay cambios
    cambio_realizado = False # Bandera para indicar si se realizó un cambio en el tablero

    # Verificar teclas numéricas del 1 al 9
    for i in range(1, 10):
        if teclas[pygame.K_1 + (i - 1)]: # Las teclas son del K_1 al K_9
            sudoku[fila][col] = i
            resultado = i # Actualiza numero ingresado
            cambio_realizado = True # Indica que hubo cambio
            break # Sale del bucle para solo permitir un cambio a la vez

    # Verificar si se presionó la tecla DELETE
    if teclas[pygame.K_DELETE]: 
        sudoku[fila][col] = 0 # Se elimina el contenido
        resultado = 0 

    # Devuelve el número ingresado (o -1 si no hubo cambio) y el estado de cambio.
    return resultado, cambio_realizado



def dibujar_tablero(ventana: pygame.display, sudoku: list[list], tablero_lleno:list[list],
                    celda_seleccionada: tuple, matriz_booleana: list[list[bool]],
                    fuente_numeros:pygame.font, FONDO_JUEGO:pygame.surface, TABLERO_ANCHO:int, TABLERO_ALTO:int,
                    BLANCO:tuple, MARGEN_IZQUIERDO:int, MARGEN_SUPERIOR:int, CELESTE:tuple, AZUL_CLARO:tuple,
                    GRIS_OSCURO:tuple, ROSA:tuple, ROSA_CLARO:tuple, tamanio_celda:int, TAMANIO_TABLERO:int,
                    NEGRO:tuple, ROJO:tuple, AZUL:tuple) -> None:
    '''
    Organiza el proceso de dibujar el tablero de Sudoku en la ventana del juego, incluyendo la configuración del fondo, el resaltado de celdas seleccionadas, 
    y el dibujo de las líneas y los números del tablero. También maneja la entrada del usuario para modificar el tablero de acuerdo a su interacción.

    Parámetros:
        ventana (pygame.display): La ventana de Pygame donde se dibujará el tablero de Sudoku.
        sudoku (list[list[int]]): La matriz que representa el estado actual del tablero de Sudoku, con los números ingresados por el usuario.
        tablero_lleno (list[list[int]]): La matriz que representa el tablero completo con la solución correcta al inicio.
        celda_seleccionada (tuple): Tupla (fila, col) que indica la celda actualmente seleccionada en el tablero (índice 0-based).
        matriz_booleana (list[list[bool]]): Una matriz que indica si un número fue ingresado por el usuario (True) o es parte del tablero inicial (False).
        fuente_numeros (pygame.font): La fuente utilizada para renderizar los números en las celdas del tablero.
        FONDO_JUEGO (pygame.Surface): El fondo que se dibuja en la ventana antes de mostrar el tablero.
        TABLERO_ANCHO (int): El ancho del tablero de Sudoku.
        TABLERO_ALTO (int): El alto del tablero de Sudoku.
        BLANCO (tuple): El color de fondo de las celdas en formato RGB (blanco).
        MARGEN_IZQUIERDO (int): El margen izquierdo de la ventana donde comienza el tablero.
        MARGEN_SUPERIOR (int): El margen superior de la ventana donde comienza el tablero.
        CELESTE (tuple): Color en formato RGB para resaltar celdas seleccionadas en celeste.
        AZUL_CLARO (tuple): Color en formato RGB para resaltar celdas seleccionadas en azul claro.
        GRIS_OSCURO (tuple): Color en formato RGB para resaltar celdas seleccionadas en gris oscuro.
        ROSA (tuple): Color en formato RGB para resaltar celdas seleccionadas en rosa.
        ROSA_CLARO (tuple): Color en formato RGB para resaltar celdas seleccionadas en rosa claro.
        tamanio_celda (int): El tamaño de cada celda del tablero en píxeles.
        TAMANIO_TABLERO (int): El tamaño total del tablero en términos de número de celdas por fila o columna.
        NEGRO (tuple): Color en formato RGB para el texto en celdas (negro).
        ROJO (tuple): Color en formato RGB para resaltar celdas con errores (rojo).
        AZUL (tuple): Color en formato RGB para resaltar celdas correctas (azul).

    Comportamiento:
        - Dibuja el fondo y el tablero en la ventana proporcionada.
        - Resalta la celda seleccionada, con un color específico dependiendo de si se ha elegido resaltar todas las celdas relacionadas o solo la celda seleccionada.
        - Dibuja las líneas del tablero, la cuadrícula y los números en las celdas, dependiendo de si son parte de la entrada del usuario o de la solución completa del Sudoku.

    Retorno:
        None: Esta función no devuelve ningún valor. Realiza las operaciones gráficas directamente sobre la ventana proporcionada.
    '''
    # Dibuja el fondo del juego
    ventana.blit(FONDO_JUEGO, [0, 0])
    
    # Dibuja fondo semitransparente
    fondo_transparente = crear_fondo_transparente(TABLERO_ANCHO, TABLERO_ALTO, BLANCO)
    ventana.blit(fondo_transparente, (MARGEN_IZQUIERDO, MARGEN_SUPERIOR))
    
    # Resalta celda seleccionada y las demas correspondientes
    if celda_seleccionada:
        fila, col = celda_seleccionada
        if not matriz_booleana[fila][col]: # Si la celda no es fija
            resaltar_celdas(ventana, fila, col, "todas", sudoku, tablero_lleno, CELESTE, AZUL_CLARO, GRIS_OSCURO,
                        ROSA, ROSA_CLARO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, tamanio_celda)
            manejar_entrada(fila, col, sudoku)
        else: # Si la celda es fija
            resaltar_celdas(ventana, fila, col, "una", sudoku, tablero_lleno, CELESTE, AZUL_CLARO, GRIS_OSCURO,
                        ROSA, ROSA_CLARO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, tamanio_celda) # Resalta con gris las que no estan permitidas modificar
    # Dibuja las cuadriculas del tablero
    dibujar_lineas(ventana, TAMANIO_TABLERO, NEGRO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, tamanio_celda, TABLERO_ANCHO, TABLERO_ALTO)
    
    # Dibuja los numeros en cada celda
    for fila in range(TAMANIO_TABLERO):
        for col in range(TAMANIO_TABLERO):
            dibujar_numero(ventana, sudoku[fila][col], fila, col, matriz_booleana, sudoku, tablero_lleno, fuente_numeros, NEGRO, ROJO, AZUL, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, tamanio_celda)


def sumar_errores(celda_seleccionada: tuple, sudoku: list[list], tablero_lleno: list[list], contador_errores:int, cambio_anterior: bool) -> int:
    '''
    Compara el valor ingresado en la celda seleccionada con el valor correspondiente en el tablero completo.

    Parámetros:
        celda_seleccionada (tuple): Coordenadas (fila, columna) de la celda actualmente seleccionada.
        sudoku (list[list]): Matriz actual del tablero de Sudoku.
        tablero_lleno (list[list]): Matriz con la solución completa del Sudoku.
        contador_errores(int): Variable inicializada.
        cambio_anterior (bool): Indica si hubo un cambio previo en la celda seleccionada.

    Retorno:
        contador_errores (int): Número de errores contabilizados.
    '''
    # Inicializar las variables de retorno
    nuevo_contador_errores = contador_errores
    nuevo_cambio_anterior = cambio_anterior

    if celda_seleccionada:  # Verifica que haya una celda seleccionada
        fila, col = celda_seleccionada
        
        # Llamar a manejar_entrada y obtener resultado y cambio_realizado
        resultado, cambio_realizado = manejar_entrada(fila, col, sudoku)

        # Solo incrementar el contador de errores si se realizó un cambio y no se contaron antes
        if cambio_realizado and not cambio_anterior:
            if resultado != tablero_lleno[fila][col] and resultado != 0:
                nuevo_contador_errores += 1

        # Actualizar el estado de cambio_anterior
        nuevo_cambio_anterior = cambio_realizado

    # Retornar el estado final de errores y cambio
    return nuevo_contador_errores, nuevo_cambio_anterior




def mostrar_texto(texto: str, x: int, y: int,ventana:pygame.display, fuente_texto: pygame.font, NEGRO:tuple) -> None: 
    '''
    Esta función muestra un texto en la ventana del juego en una posición específica.

    Parámetros:
        texto (str): El texto que se desea mostrar.
        x (int): La coordenada horizontal donde se dibujará el texto.
        y (int): La coordenada vertical donde se dibujará el texto.
        ventana (pygame.display): La ventana de Pygame donde se mostrará el texto.
        fuente_texto (pygame.font): La fuente utilizada para renderizar el texto.
        NEGRO: El color de fondo en formato RGB.

    Retorno:
        None: Esta función no devuelve ningún valor.
    '''
    texto_superficie = fuente_texto.render(texto, True, NEGRO)
    ventana.blit(texto_superficie, (x, y))
    return texto_superficie

def evento_click(x: int, y: int, w: int, h: int) -> bool:
    '''
    Esta función detecta si cliqueamos dentro de un área rectangular específica en la ventana del juego.
        Recibe:
        x (int): Coordenada horizontal del inicio del rectángulo.
        y (int): Coordenada vertical del inicio del rectángulo.
        w (int): Ancho del rectangulo.
        h (int): Altura del rectangulo.
        Devuelve:
        bool: True si se detecta un clic dentro del area, False en caso contrario.
    '''
    click = False
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h and mouse_click[0]:
        click = True
        
    return click


def mostrar_menu_principal(ventana:pygame.display, dificultad:str, FONDO: pygame.surface, NEGRO:tuple, fuente_texto:pygame.font, AMARILLO_CLARO:tuple, VALOR_BORDER_RADIUS:int, AMARILLO_OSCURO:tuple,BLANCO:tuple) -> None:
    '''
    Esta función dibuja el menú principal en la ventana del juego, mostrando el título y botones de opciones.

    Parámetros:
        ventana (pygame.display): La ventana donde se dibuja el menú principal.
        VALOR_BORDER_RADIUS (int): Radio del botón.
        dificultad (str): El texto que indica el nivel de dificultad que se mostrará en un botón del menú.
        FONDO(pygame.surface): Constante que contiene la imagen de fondo.
        NEGRO (tuple): Color utilizado para el texto del título.
        fuente_texto (pygame.font): Fuente utilizada para renderizar los botones del menú.

    Retorno:
        None: Esta función no devuelve ningún valor.
    '''
    ventana.blit(FONDO, [0,0])


    mostrar_boton("Jugar", 565, 220, 150, 50,ventana,fuente_texto, AMARILLO_CLARO,NEGRO,VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)
    mostrar_boton("Puntajes", 565, 280, 150, 50,ventana,fuente_texto, AMARILLO_CLARO,NEGRO,VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)
    mostrar_boton(dificultad, 565, 340, 150, 50,ventana,fuente_texto, AMARILLO_CLARO,NEGRO,VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)
    mostrar_boton("Salir", 565, 400, 150, 50,ventana,fuente_texto, AMARILLO_CLARO,NEGRO,VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)
    
    
    pygame.display.update()

def mostrar_popup_perdido(ventana:pygame.display, fuente_texto:pygame.font, VALOR_BORDER_RADIUS:int, ROJO:tuple, BLANCO:tuple):
    """
    Muestra un pop-up centrado en la pantalla indicando que el jugador ha perdido.

    Parámetros:
        ventana (pygame.Surface): La ventana donde se mostrará el pop-up.
        fuente_texto (pygame.font.Font): Fuente utilizada para el texto del pop-up.
        VALOR_BORDER_RADIUS (int): Valor del radio.
        ROJO (tuple): Color del fondo del pop-up.
        BLANCO (tuple): Color del texto en el pop-up.
    """
    # Fondo negro
    #ventana.fill(NEGRO)

    # Definir el rectángulo del pop-up
    popup_rect = pygame.Rect(200, 200, 400, 200)
    pygame.draw.rect(ventana, ROJO, popup_rect, border_radius=VALOR_BORDER_RADIUS)  # Fondo rojo del pop-up

    # Agregar el texto de "¡PERDISTE!" centrado en la parte superior del pop-up
    texto_perdido = fuente_texto.render("¡PERDISTE!", True, BLANCO)
    texto_x1 = popup_rect.centerx - texto_perdido.get_width() // 2
    texto_y1 = popup_rect.top + 65  # Posición del primer texto (ajústalo según desees)
    ventana.blit(texto_perdido, (texto_x1, texto_y1))

    # Agregar el texto "Volviendo al menú principal en 3..2..1.." centrado más abajo
    texto_perdido_dos = fuente_texto.render("Volviendo al menú principal en 3..2..1..", True, BLANCO)
    texto_x2 = popup_rect.centerx - texto_perdido_dos.get_width() // 2
    texto_y2 = texto_y1 + texto_perdido.get_height() + 20  # Separación entre ambos textos
    ventana.blit(texto_perdido_dos, (texto_x2, texto_y2))

def mostrar_popup_ganaste(ventana: pygame.Surface, fuente_texto: pygame.font.Font, 
                          VALOR_BORDER_RADIUS: int, VERDE: tuple, BLANCO: tuple, archivo_json: str, puntaje_final: int) -> bool:
    """
    Muestra un pop-up verde donde se indica que el jugador ganó e incluye un input para ingresar el nombre.
    El nombre ingresado se guarda en un archivo JSON. Regresa True una vez que el jugador ingresa el nombre.

    Parámetros:
        ventana (pygame.Surface): La ventana donde se mostrará el pop-up.
        fuente_texto (pygame.font.Font): Fuente utilizada para los textos del pop-up.
        VALOR_BORDER_RADIUS (int): Radio para las esquinas del pop-up.
        VERDE (tuple): Color del fondo del pop-up.
        BLANCO (tuple): Color del texto en el pop-up.
        archivo_json (str): Ruta del archivo JSON donde se guardará el nombre.
        puntaje_final (int): Puntaje final del jugador que será guardado.

    Retorno:
        bool: Devuelve True si se ingresó el nombre y se guardó correctamente.
    """
    activo = True
    user_text = ""  # Para almacenar el texto ingresado
    clock = pygame.time.Clock()
    resultado = False  # Variable para el estado final

    # Rectángulo del pop-up
    popup_rect = pygame.Rect(200, 200, 400, 250)
    input_rect = pygame.Rect(220, 350, 360, 40)  # Rectángulo del input

    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Salir del juego
                pygame.quit()
                activo = False
                resultado = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Guardar nombre al presionar Enter
                    if user_text != "":
                        guardar_jugador(archivo_json, user_text, puntaje_final)
                        activo = False
                        resultado = True  # Proceso exitoso
                    else:
                        guardar_jugador(archivo_json, "Sin nombre", puntaje_final)
                        activo = False
                        resultado = True  # Proceso exitoso
                elif evento.key == pygame.K_BACKSPACE:  # Borrar última letra
                    user_text = user_text[:-1]
                else:  # Agregar texto
                    user_text += evento.unicode

        # Dibujar el fondo y el pop-up
        pygame.draw.rect(ventana, VERDE, popup_rect, border_radius=VALOR_BORDER_RADIUS)

        # Mensaje "¡GANASTE!"
        texto_ganaste = fuente_texto.render("¡GANASTE!", True, BLANCO)
        texto_x1 = popup_rect.centerx - texto_ganaste.get_width() // 2
        texto_y1 = popup_rect.top + 65
        ventana.blit(texto_ganaste, (texto_x1, texto_y1))

        # Mensaje "Ingresá tu nombre"
        texto_input = fuente_texto.render("Ingresá tu nombre:", True, BLANCO)
        texto_x2 = popup_rect.centerx - texto_input.get_width() // 2
        texto_y2 = texto_y1 + texto_ganaste.get_height() + 40
        ventana.blit(texto_input, (texto_x2, texto_y2))

        # Dibujar el cuadro de texto
        pygame.draw.rect(ventana, BLANCO, input_rect, border_radius=5)
        texto_ingresado = fuente_texto.render(user_text, True, (0, 0, 0))  # Texto del input
        ventana.blit(texto_ingresado, (input_rect.x + 10, input_rect.y + 10))  # Margen dentro del input

        pygame.display.update()
        clock.tick(30)  # Controlar la velocidad del bucle

    return resultado
        

    
def actualizar_ultimo_click_dificultad(ultimo_clic:int, DELAY_CLIC:int) -> int:
    '''
    Actualiza el tiempo del último clic en el botón de dificultad, asegurando que 
    se respete un retraso mínimo entre clics consecutivos.

    Parámetros:
        ultimo_clic (int): El tiempo registrado del último clic en milisegundos.
        DELAY_CLIC (int): El retraso mínimo permitido entre clics consecutivos.

    Retorno:
        int: El tiempo del clic actual, si se permite actualizar; de lo contrario, 
        se retorna el valor original de `ultimo_clic`.
    '''
    tiempo_actual = pygame.time.get_ticks() # Devuelve el tiempo que transcurrió desde que se inicio el programa
    if tiempo_actual - ultimo_clic > DELAY_CLIC:
        # Guardar el tiempo del clic actual
        ultimo_clic_dificultad = tiempo_actual
    
    return ultimo_clic_dificultad


def cambiar_dificultad(ultimo_clic_dificultad, dificultad, DELAY_CLIC: int, ventana: pygame.display, BLANCO:tuple, GRIS:tuple, VALOR_BORDER_RADIUS: int, fuente_texto:pygame.font, NEGRO:tuple) -> str:
    '''
    Cambia la dificultad del juego cíclicamente entre "Fácil", "Medio" y "Difícil" al presionar el botón correspondiente.
    Controla el tiempo entre clics para evitar cambios repetitivos en intervalos cortos.

    Parámetros:
        ultimo_clic_dificultad (int): Marca de tiempo en milisegundos del último clic registrado.
        dificultad (str): La dificultad actual del juego, puede ser "Facil", "Medio" o "Dificil".
        DELAY_CLIC (int): El retraso mínimo permitido entre clics consecutivos.
        ventana (pygame.display): La ventana de Pygame donde se actualiza el botón de dificultad.
        BLANCO (tuple) : Color de fondo cuando borra
        GRIS (tuple): Colo nuevo generado cuando redibuja
        VALOR_BORDER_RADIUS (int): El radio del boton

    Retorno:
        str: La nueva dificultad seleccionada ("Fácil", "Medio" o "Difícil").
    '''
    tiempo_actual = pygame.time.get_ticks() # Devuelve el tiempo que transcurrió desde que se inicio el programa
    
    # Verificar si han pasado los 500 milisegundos desde el último clic
    if tiempo_actual - ultimo_clic_dificultad > DELAY_CLIC:
        # Cambiar la dificultad
        if dificultad == "Facil":
            dificultad = "Medio"
            print(dificultad)
        elif dificultad == "Medio":
            dificultad = "Dificil"
            print(dificultad)
            
        else:
            dificultad = "Facil"
            print(dificultad)
            
        
        # Actualizar el botón de dificultad
        actualizar_boton_dificultad(ventana,dificultad,BLANCO, GRIS, VALOR_BORDER_RADIUS,fuente_texto,NEGRO)
        
        # Guardar el tiempo del clic actual
        ultimo_clic_dificultad = actualizar_ultimo_click_dificultad(ultimo_clic_dificultad, DELAY_CLIC)
        
    return dificultad


def actualizar_boton_dificultad(ventana:pygame.display, dificultad:str, BLANCO:tuple, GRIS:tuple, VALOR_BORDER_RADIUS:int, fuente_texto:pygame.font, NEGRO:tuple) -> None: 
    '''
    Esta función actualiza el botón de dificultad en la interfaz de usuario, 
    cambiando el texto del botón según la dificultad seleccionada.
    
    Primero limpia el área del botón y luego lo redibuja con el nuevo texto de la dificultad.
    
        Recibe:
        ventana(pygame.display): La ventana donde se dibuja el menú principal.
        dificultad(str): La dificultad actual del juego, puede ser "Facil", "Medio" o "Dificil".
        BLANCO (tuple) : Color de fondo cuando borra
        GRIS (tuple): Colo nuevo generado cuando redibuja
        VALOR_BORDER_RADIUS (int): El radio del boton
        Devuelve:
        None
    '''
    # Limpiar toda el área del botón
    x, y, ancho, alto = 550, 330, 150, 50  # Coordenadas del botón
    pygame.draw.rect(ventana, BLANCO, (x, y, ancho, alto), border_radius=VALOR_BORDER_RADIUS)  # Borra el área del botón
    
    # Redibujar el botón con el nuevo texto
    pygame.draw.rect(ventana, GRIS, (x, y, ancho, alto), border_radius=VALOR_BORDER_RADIUS)  # Fondo del botón
    mostrar_texto(dificultad, x + ancho // 2 - fuente_texto.size(dificultad)[0] // 2, y + alto // 2 - fuente_texto.size(dificultad)[1] // 2,ventana, fuente_texto, NEGRO)
    pygame.display.update()

def mostrar_boton(texto: str, x: int, y: int, ancho: int, alto: int, ventana:pygame.display,
                fuente_texto:pygame.font, AMARILLO_CLARO:tuple, NEGRO:tuple, VALOR_BORDER_RADIUS:int, grosor_borde: int, AMARILLO_OSCURO:tuple) -> None:
    '''
    Esta función dibuja un botón en la interfaz.

    Primero dibuja el rectángulo del botón en la ventana con un fondo de color azul claro, luego coloca el texto en el centro del botón.

    Parámetros:
    texto (str): El texto que se mostrará en el botón.
    x (int): La coordenada X de la esquina superior izquierda del botón.
    y (int): La coordenada Y de la esquina superior izquierda del botón.
    ancho (int): El ancho del botón.
    alto (int): El alto del botón.
    ventana (pygame.display): La ventana donde se dibuja el botón.
    fuente_texto (pygame.font): La fuente utilizada para renderizar el texto del botón.
    AZUL_CLARO (tuple): El color de fondo del botón, representado como una tupla de 3 valores RGB.
    NEGRO (tuple): El color del texto, representado como una tupla de 3 valores RGB.
    VALOR_BORDER_RADIUS (int): El valor que define el radio de redondeo de los bordes del botón.

    Devuelve:
    None: Esta función no devuelve ningún valor.
    '''
    
    cursor_x, cursor_y = pygame.mouse.get_pos()
    
    if cursor_x > x and cursor_x < (x + ancho) and cursor_y > y and cursor_y < (y + alto):
        pygame.draw.rect(ventana, AMARILLO_OSCURO, (x, y, ancho, alto), border_radius=VALOR_BORDER_RADIUS)
    else:    
        pygame.draw.rect(ventana, AMARILLO_CLARO, (x, y, ancho, alto), border_radius=VALOR_BORDER_RADIUS)
    
    # Dibuja el borde del botón con el grosor indicado
    pygame.draw.rect(ventana, NEGRO, (x, y, ancho, alto), grosor_borde, border_radius=VALOR_BORDER_RADIUS)

    # Calcula el tamaño del texto
    texto_superficie = fuente_texto.render(texto, True, NEGRO)
    texto_ancho = texto_superficie.get_width()
    texto_alto = texto_superficie.get_height()
    
    # Dibuja el texto centrado en el boton
    ventana.blit(texto_superficie, (x + (ancho - texto_ancho) // 2, y + (alto - texto_alto) // 2))

def jugar(sudoku:list[list], dificultad: str, ventana:pygame.display, tablero_lleno:list[list[int]], celda_seleccionada: tuple, matriz_booleana: list[list[bool]], fuente_numeros: pygame.font, 
          temporizador: int, contador_errores: int, fuente_texto: pygame.font, BLANCO: tuple, FONDO: pygame.Surface, 
          TABLERO_ANCHO: int, TABLERO_ALTO: int, MARGEN_IZQUIERDO: int, MARGEN_SUPERIOR: int, CELESTE: tuple, 
          AMARILLO_CLARO: tuple, GRIS_OSCURO: tuple, ROSA: tuple, ROSA_CLARO: tuple, tamanio_celda: int, 
          TAMANIO_TABLERO: int, NEGRO: tuple, ROJO: tuple, AZUL: tuple, VALOR_BORDER_RADIUS: int, AMARILLO_OSCURO:tuple) -> list[list]:
    '''
    Inicia una nueva partida de Sudoku generando un tablero según la dificultad seleccionada
    y actualiza la pantalla del juego.

    Parámetros:
        sudoku (list[list]): El tablero de Sudoku inicial.
        dificultad (str): Nivel de dificultad del juego ('Facil', 'Medio', 'Dificil').
        ventana (pygame.display): La ventana de Pygame donde se mostrará el juego.
        tablero_lleno (list[list[int]]): La matriz que representa el tablero completo al inicio (sin cambios del usuario).
        celda_seleccionada (tuple): Coordenadas de la celda seleccionada en el tablero.
        matriz_booleana (list[list[bool]]): Matriz que indica las celdas activas o seleccionadas.
        fuente_numeros (pygame.font): Fuente utilizada para renderizar los números del tablero.
        temporizador (int): Tiempo transcurrido o restante en el juego.
        contador_errores (int): Cantidad de errores cometidos por el jugador.
        fuente_texto (pygame.font): Fuente utilizada para renderizar texto como botones o mensajes.
        BLANCO (tuple): Color RGB para el fondo de la ventana.
        FONDO (pygame.Surface): Superficie de fondo utilizada en la pantalla.
        TABLERO_ANCHO (int): Ancho del tablero de Sudoku.
        TABLERO_ALTO (int): Alto del tablero de Sudoku.
        MARGEN_IZQUIERDO (int): Margen izquierdo del tablero en píxeles.
        MARGEN_SUPERIOR (int): Margen superior del tablero en píxeles.
        CELESTE (tuple): Color RGB para resaltar celdas seleccionadas.
        AMARILLO_CLARO (tuple): Color RGB para resaltar celdas activas o correctas.
        GRIS_OSCURO (tuple): Color RGB para resaltar celdas deshabilitadas o vacías.
        ROSA (tuple): Color RGB para celdas incorrectas.
        ROSA_CLARO (tuple): Color RGB para resaltar celdas con errores leves.
        tamanio_celda (int): Tamaño de cada celda en píxeles.
        TAMANIO_TABLERO (int): Dimensiones del tablero (número de celdas por lado).
        NEGRO (tuple): Color RGB para el texto principal (números).
        ROJO (tuple): Color RGB para errores graves.
        AZUL (tuple): Color RGB para resaltar celdas correctas.
        VALOR_BORDER_RADIUS (int): Radio de redondeo de los bordes de los botones.

    Retorno:
        list[list]: Un tablero de Sudoku generado de acuerdo a la dificultad seleccionada.
    '''

    # Generar un nuevo tablero basado en la dificultad
    sudoku = generar_sudoku(tablero_lleno, dificultad)
    
    
    # Actualizar la pantalla del juego con el nuevo tablero
    mostrar_pantalla_juego(sudoku,ventana, tablero_lleno, celda_seleccionada, matriz_booleana, fuente_numeros, temporizador, contador_errores, fuente_texto, BLANCO,
                            FONDO, TABLERO_ANCHO, TABLERO_ALTO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, CELESTE, AMARILLO_CLARO, GRIS_OSCURO,
                            ROSA, ROSA_CLARO, tamanio_celda, TAMANIO_TABLERO, NEGRO, ROJO, AZUL, VALOR_BORDER_RADIUS, AMARILLO_OSCURO)
    
    return sudoku

def mostrar_pantalla_juego(sudoku: list[list], ventana:pygame.display, tablero_lleno:list[list[int]],
                            celda_seleccionada:tuple, matriz_booleana: list[list[bool]],
                              fuente_numeros:pygame.font, temporizador:int, contador_errores:int,
                                fuente_texto:pygame.font, BLANCO: tuple,
                            FONDO_JUEGO: pygame.Surface, TABLERO_ANCHO: int, TABLERO_ALTO: int, MARGEN_IZQUIERDO: int,
                            MARGEN_SUPERIOR: int, CELESTE: tuple, AMARILLO_CLARO: tuple, GRIS_OSCURO: tuple,
                            ROSA: tuple, ROSA_CLARO: tuple, tamanio_celda: int, TAMANIO_TABLERO: int, NEGRO: tuple,
                            ROJO: tuple, AZUL: tuple, VALOR_BORDER_RADIUS: int, AMARILLO_OSCURO:tuple) -> None:
    '''
        Parámetros:
        sudoku (list[list[int]]): Una matriz bidimensional que representa el estado actual del tablero de Sudoku.
        ventana (pygame.display): La ventana donde se dibuja la interfaz del juego.
        tablero_lleno (list[list[int]]): Una matriz bidimensional que indica las celdas llenas en el tablero.
        celda_seleccionada (tuple): Las coordenadas de la celda seleccionada en el tablero.
        matriz_booleana (list[list[bool]]): Una matriz que indica si una celda está activa o seleccionada.
        fuente_numeros (pygame.font): La fuente utilizada para renderizar los números en el tablero.
        temporizador (int): El valor del temporizador que se muestra en la interfaz del juego.
        contador_errores (int): El contador de errores cometidos durante el juego.
        fuente_texto (pygame.font): La fuente utilizada para renderizar el texto de los botones.
        BLANCO (tuple): Color en formato RGB para el fondo de la ventana.
        FONDO_JUEGO (pygame.Surface): Superficie que representa el fondo de la ventana.
        TABLERO_ANCHO (int): El ancho del tablero de Sudoku.
        TABLERO_ALTO (int): El alto del tablero de Sudoku.
        MARGEN_IZQUIERDO (int): El margen izquierdo del tablero.
        MARGEN_SUPERIOR (int): El margen superior del tablero.
        CELESTE (tuple): Color en formato RGB para resaltar celdas seleccionadas en celeste.
        AMARILLO_CLARO (tuple): Color en formato RGB para resaltar celdas seleccionadas en azul claro.
        GRIS_OSCURO (tuple): Color en formato RGB para resaltar celdas seleccionadas en gris oscuro.
        ROSA (tuple): Color en formato RGB para resaltar celdas seleccionadas en rosa.
        ROSA_CLARO (tuple): Color en formato RGB para resaltar celdas seleccionadas en rosa claro.
        tamanio_celda (int): El tamaño de cada celda del tablero en píxeles.
        TAMANIO_TABLERO (int): El tamaño total del tablero en términos de número de celdas por fila o columna.
        NEGRO (tuple): Color en formato RGB para el texto en celdas (negro).
        ROJO (tuple): Color en formato RGB para resaltar celdas con errores (rojo).
        AZUL (tuple): Color en formato RGB para resaltar celdas correctas (azul).
        VALOR_BORDER_RADIUS (int): Valor del radio de borde de los botones.
        AMARILLO_OSCURO (tuple): Color del sombreado del botón.
    
    Retorno:
        None: Esta función no devuelve ningún valor.

    '''
    ventana.fill(BLANCO)
    dibujar_tablero(ventana,sudoku, tablero_lleno,celda_seleccionada, matriz_booleana, fuente_numeros,FONDO_JUEGO, TABLERO_ANCHO, TABLERO_ALTO,
                       BLANCO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, CELESTE, AMARILLO_CLARO, GRIS_OSCURO, ROSA, ROSA_CLARO,
                         tamanio_celda, TAMANIO_TABLERO, NEGRO, ROJO, AZUL)
    
    mostrar_temporizador(temporizador,ventana,fuente_texto,NEGRO)
    mostrar_contador_errores(contador_errores, ventana,fuente_texto, NEGRO)  
    mostrar_boton("Volver", 1060, 600, 170, 60,ventana,fuente_texto,AMARILLO_CLARO,NEGRO,VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)
    mostrar_boton("Reiniciar", 1060, 530, 170, 60,ventana,fuente_texto,AMARILLO_CLARO,NEGRO,VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)

    pygame.display.update()


def mostrar_contador_errores(errores:int,ventana:pygame.display,fuente_texto:pygame.font, NEGRO:tuple) -> None:
    '''
    Esta función muestra el contador de errores en la pantalla, indicando cuántos errores 
    ha cometido el jugador hasta el momento.

    El contador de errores se dibuja en la esquina superior derecha de la ventana, 
    utilizando un color verde amarillento.

    Parámetros:
    errores (int): El número de errores cometidos por el jugador hasta el momento. 
                    Este valor se muestra en la pantalla.
    ventana (pygame.display): La ventana donde se dibuja la interfaz del juego.
    NEGRO (pygame.font): Color de la letra negro

    Devuelve:
    None
    '''
    
    texto_errores = fuente_texto.render(f"Errores: {errores}", True, NEGRO)
    ventana.blit(texto_errores, (1070, 158))  # Mostrar el contador en la posición deseada

def mostrar_temporizador(temporizador:int, ventana: pygame.display, fuente_texto:pygame.font, NEGRO:pygame.font) -> int:
    '''
    Esta función muestra el temporizador en la pantalla, indicando el tiempo transcurrido 
    desde el inicio del juego en formato minutos:segundos.

    El tiempo se muestra en la esquina superior derecha de la ventana, 
    utilizando un color verde amarillento.

    Parámetros:
    temporizador (int): El tiempo transcurrido en segundos desde que comenzó el juego. 
                        Este valor se convierte en minutos y segundos para ser mostrado.
    ventana (pygame.display): La ventana donde se dibuja el juego.
    fuente_texto (pygame.font): Fuente predeterminada del texto.
    NEGRO (pygame.font): Color del texto

    Devuelve:
    None
    '''
    minutos = temporizador // 60
    segundos = temporizador % 60
    tiempo_texto = fuente_texto.render(f"Tiempo: {minutos}:{segundos:02}", True, NEGRO)
    ventana.blit(tiempo_texto, (1070, 72))  # Ajusta la posición según el diseño de tu ventana
    
    return minutos

def ver_puntajes(ventana:pygame.display, fuente_texto:pygame.font, FONDO_PANTALLA_GANADORES:pygame.surface,
                NEGRO:tuple,AZUL_CLARO:tuple,VALOR_BORDER_RADIUS:int,AMARILLO_OSCURO:tuple, nombre_archivo:str, BLANCO:tuple) -> None:
    """
    Muestra en la pantalla los 5 mejores puntajes almacenados, 
    con los nombres de los jugadores y sus puntajes. 

    El listado de puntajes se obtiene a través de la función `leer_puntajes`.
    La información es mostrada en la ventana del juego, con un botón para 
    volver al menú principal.

    Parámetros:
    ventana(pygame.display): La ventana donde se dibujan los puntajes.
    fuente_texto(pygame.font): La fuente del texto.
    FONDO_PANTALLA_GANADORES (pygame.surface) : Fondo de pantalla.
    NEGRO:(tuple): Color de la fuente
    AZUL_CLARO(tuple): Color del botonm
    VALOR_BORDER_RADIUS(int): valor del radio.
    AMARILLO_OSCURO(tuple): color de la sobra del botón.

    Devuelve:
    None
    """
    lista_puntajes = mostrar_archivo(nombre_archivo) # Trae los puntajes del archivo
    ventana.blit(FONDO_PANTALLA_GANADORES, [0, 0]) # Genera el fondo a partir de archivo
    y_pos = 270 # Donde inicia la lista top 5
    for jugador in lista_puntajes[:5]:
        nombre = jugador.get("nombre", "Sin nombre")
        puntaje = jugador.get("puntaje", 0)
        mostrar_texto(f"{nombre}: {puntaje}", 550, y_pos, ventana, fuente_texto, BLANCO)
        y_pos += 55
    mostrar_boton("Volver", 550, 550, 150, 50, ventana, fuente_texto, AZUL_CLARO, NEGRO, VALOR_BORDER_RADIUS,1,AMARILLO_OSCURO)
    pygame.display.update()



def calcular_puntaje(dificultad:str, PUNTOS_BASE:int, contador_errores:int, PENALIZACION_ERROR:int, minutos:int, PENALIZACION_TIEMPO:int) -> int:
    '''
    Calcula el puntaje dependiendo la cantidad de errores, el tiempo tardado y la dificultad seleccionada
    
    Puntaje = (Puntos Base - (Errores x Penalización por Error) - (Tiempo Transcurrido en Minutos x Penalización por Tiempo)) x Dificultad
    Puntaje = (Puntos Base - (Errores x Penalización por Error) - (Tiempo Transcurrido en Minutos x
    Penalización por Tiempo)) x Dificultad
    Parametros:
    PUNTOS_BASE (int): Es el puntaje inicial que se le da al jugador al comenzar la partida. Por ej 1000 puntos.
    contador_errores(int): Es la cantidad de errores cometidos por el jugador durante la partida.
    PENALIZACION_ERROR(int): Un valor que se resta por cada error. Por ejemplo, 50 puntos por error.
    minutos(int): Tiempo transcurrido entre el inicio y la finalización de la partida.
    PENALIZACION_TIEMPO(int): Un valor que se resta por cada minuto. Por ejemplo, 10 puntos por minuto.
    dificultad(str): Un multiplicador en función de la dificultad seleccionada.

    Devuelve: El calculo mencionado en la documentación
    
    ''' 

    if dificultad == "Facil":
        multiplicador_dificultad = 1
    elif dificultad == "Medio":
        multiplicador_dificultad = 1.5
    else:
        multiplicador_dificultad = 2
        
    puntaje_final = (PUNTOS_BASE - (contador_errores * PENALIZACION_ERROR) - (minutos * PENALIZACION_TIEMPO)) * multiplicador_dificultad
    
    if puntaje_final < 0:
        puntaje_final = 0
    
    return int(puntaje_final)




def salir() -> None:
    """
    Finaliza la ejecución del juego y cierra la ventana de Pygame.

    Esta función se encarga de cerrar correctamente la ventana del juego
    y terminar la ejecución del programa.

    Parámetros: Ninguno

    Devuelve: None
    """
    pygame.quit()
    exit()