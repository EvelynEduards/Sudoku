from biblioteca import *
import pygame
from configuraciones  import *
from logica_sodoku import *
from puntaje import *


# Inicializar pygame
pygame.init()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salir()

        musica.play()  # Comienza la música al iniciar el bucle principal

        # Manejo de eventos del temporizador
        if evento.type == pygame.USEREVENT:  # Evento personalizado cada segundo
            temporizador += 1  # Incrementa el tiempo en segundos                        
                            
        # Manejo de clics según la pantalla actual
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if pantalla_actual == "menu":
                if evento_click(565, 220, 150, 50):  # Botón "Jugar"
                    temporizador = 0 # Reincia temporizador
                    pantalla_actual = "juego"
                    tablero_lleno = generar_tablero()
                    sudoku = jugar(tablero_lleno, dificultad,ventana,tablero_lleno, celda_seleccionada, matriz_booleana, fuente_numeros, 
                                    temporizador, contador_errores, fuente_texto, BLANCO, FONDO_JUEGO, TABLERO_ANCHO, TABLERO_ALTO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, CELESTE, 
                                    AMARILLO_CLARO, GRIS_OSCURO, ROSA, ROSA_CLARO, tamanio_celda, TAMANIO_TABLERO, NEGRO, ROJO, AZUL, VALOR_BORDER_RADIUS,AMARILLO_OSCURO)
                    matriz_booleana = generar_matriz_booleana(sudoku)
                elif evento_click(565, 280, 150, 50):  # Botón "Puntajes"
                    pantalla_actual = "puntajes"
                    ver_puntajes(ventana, fuente_texto, FONDO_PANTALLA_GANADORES, NEGRO, AZUL_CLARO, VALOR_BORDER_RADIUS, AMARILLO_OSCURO,"nombre_ganadores.json", BLANCO)
                elif evento_click(565, 340, 150, 50):  # Botón "Dificultad"
                    dificultad =  cambiar_dificultad(ultimo_clic_dificultad,dificultad, DELAY_CLIC, ventana, BLANCO, GRIS, VALOR_BORDER_RADIUS,fuente_texto, NEGRO)
                    tablero_lleno = generar_tablero()
                    sudoku = jugar(tablero_lleno, dificultad,ventana,tablero_lleno, celda_seleccionada, matriz_booleana, fuente_numeros, 
                                    temporizador, contador_errores, fuente_texto, BLANCO, FONDO_JUEGO, TABLERO_ANCHO, TABLERO_ALTO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, CELESTE, 
                                        AMARILLO_CLARO, GRIS_OSCURO, ROSA, ROSA_CLARO, tamanio_celda, TAMANIO_TABLERO, NEGRO, ROJO, AZUL, VALOR_BORDER_RADIUS,AMARILLO_OSCURO)
                    matriz_booleana = generar_matriz_booleana(sudoku)
                elif evento_click(565, 400, 150, 50):  # Botón "Salir"
                    salir()
            elif pantalla_actual == "juego": 
                x, y = pygame.mouse.get_pos()
                if MARGEN_IZQUIERDO <= x <= MARGEN_IZQUIERDO + TABLERO_ANCHO and MARGEN_SUPERIOR <= y <= MARGEN_SUPERIOR + TABLERO_ALTO: #Mouse adentro del tablero
                    col = (x - MARGEN_IZQUIERDO) // tamanio_celda
                    fila = (y - MARGEN_SUPERIOR) // tamanio_celda
                    celda_seleccionada = (fila, col) # Genera tupla de la celda seleccionada a partir de las coordenada del get_pos
                elif evento_click(1060, 530, 170, 60): #Botón "Reiniciar"
                    sudoku = jugar(tablero_lleno, dificultad,ventana,tablero_lleno, celda_seleccionada, matriz_booleana, fuente_numeros, 
                                    temporizador, contador_errores, fuente_texto, BLANCO, FONDO_JUEGO, TABLERO_ANCHO, TABLERO_ALTO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, CELESTE, 
                                    AMARILLO_CLARO, GRIS_OSCURO, ROSA, ROSA_CLARO, tamanio_celda, TAMANIO_TABLERO, NEGRO, ROJO, AZUL, VALOR_BORDER_RADIUS,AMARILLO_OSCURO)
                    tablero_lleno = generar_tablero()
                    matriz_booleana = generar_matriz_booleana(sudoku)
                    contador_errores = 0 # Reinicia contador de errores
                    temporizador = 0 # Reincia temporizador
                elif evento_click(1060, 600, 170, 60):  # Botón "Volver" dentro de la pantalla juego
                    pantalla_actual = "menu"
                else:
                    celda_seleccionada = None #Si hace click en un lugar que no sea una celda o botón, saca el click de la celda o no marca nada.
            elif pantalla_actual == "puntajes":
                if evento_click(550, 550, 150, 50):  # Botón "Volver"
                    pantalla_actual = "menu"
            
    # Actualizar la pantalla según el estado
    if pantalla_actual == "menu":
        mostrar_menu_principal(ventana, dificultad, FONDO, NEGRO, fuente_texto,AMARILLO_CLARO, VALOR_BORDER_RADIUS, AMARILLO_OSCURO,BLANCO)
        contador_errores = 0 #para que funcione el pop up de errores
    elif pantalla_actual == "juego":
        if contador_errores == None:
            contador_errores = 0
        contador_errores, cambio_anterior = sumar_errores(celda_seleccionada, sudoku, tablero_lleno, contador_errores, cambio_anterior)
        if contador_errores > 3 and not mostrar_popup: #porque sino se repite en el bucle muchas veces el pop up
            mostrar_popup = True
            tiempo_inicio_popup = pygame.time.get_ticks()
    # Si hay un pop-up activo, dibujarlo
        if mostrar_popup:
            mostrar_popup_perdido(ventana, fuente_texto, VALOR_BORDER_RADIUS, ROJO, BLANCO)
            pygame.display.update()  # Actualizar pantalla cada vez que el pop-up esté activo
        # Verificar si el tiempo del pop-up ha pasado
            if pygame.time.get_ticks() - tiempo_inicio_popup > duracion_popup:
                pantalla_actual = "menu"  # Cambiar al menú principal
                mostrar_popup = False
        else:
            mostrar_pantalla_juego(sudoku, ventana, tablero_lleno, celda_seleccionada, matriz_booleana, fuente_numeros, temporizador, contador_errores, fuente_texto, BLANCO,
                            FONDO_JUEGO, TABLERO_ANCHO, TABLERO_ALTO, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, CELESTE, AMARILLO_CLARO, GRIS_OSCURO,
                            ROSA, ROSA_CLARO, tamanio_celda, TAMANIO_TABLERO, NEGRO, ROJO, AZUL, VALOR_BORDER_RADIUS, AMARILLO_OSCURO)
            minutos = mostrar_temporizador(temporizador, ventana,fuente_texto, NEGRO)  # Mostrar el temporizador solo en la pantalla del juego
        if sudoku == tablero_lleno:
            puntaje_jugador = calcular_puntaje(dificultad, PUNTOS_BASE, contador_errores, PENALIZACION_ERROR, minutos, PENALIZACION_TIEMPO)
            pantalla_actual = "ganaste"  # Cambiar al estado de ganaste
    elif pantalla_actual == "ganaste":
    # Mostrar pop-up para ingresar el nombre
        if mostrar_popup_ganaste(ventana, fuente_texto, VALOR_BORDER_RADIUS, VERDE, BLANCO, "nombre_ganadores.json", puntaje_jugador):
            pantalla_actual = "puntajes"  # Cambiar al estado de puntajes

    elif pantalla_actual == "puntajes":
        ver_puntajes(ventana, fuente_texto, FONDO_PANTALLA_GANADORES, NEGRO, AZUL_CLARO, VALOR_BORDER_RADIUS, AMARILLO_OSCURO, "nombre_ganadores.json", BLANCO)

    pygame.display.update()

pygame.quit()