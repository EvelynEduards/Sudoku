import pygame
pygame.init()
from biblioteca import *
from logica_sodoku import *


# ==============================
# Configuraciones del Tablero
# ==============================
TAMANIO_TABLERO = 9
MARGEN_IZQUIERDO = 150 # Margen de 50px para la izquierda del tablero
MARGEN_SUPERIOR = 100 # Margen de 50px para arriba del tablero


# ==============================
# Configuraciones la Ventana
# ==============================
FONDO = pygame.image.load("fondo sudoku/Frame 2.jpg") #se importa la imagen de fondo del juego de la carpeta de fondo sudoku
FONDO_PANTALLA_GANADORES = pygame.image.load("fondo sudoku/PANTALLA_PUNTAJE.jpg")
FONDO_JUEGO = pygame.image.load("fondo sudoku/PANTALLA_JUEGO.jpg")
ventana = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Sudoku")
TABLERO_ANCHO = 540
TABLERO_ALTO = 540


# ==============================
# Colores
# ==============================
ROJO_CLARO = (255, 102, 102)
AMARILLO_MAS_CLARO = (255, 223, 0)
AMARILLO_CLARO = (255,255,207)
AMARILLO_OSCURO = (200, 180, 90)
BLANCO = (255, 255, 255)
NEGRO = (33,33,33)
GRIS = (200, 200, 200)
GRIS_OSCURO = (160, 160, 160)
CELESTE = (175, 215, 230)
AZUL_CLARO = (135, 205, 250)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
BLANCO_GRISACEO = (158, 169, 177)
ROSA = (255, 200, 200)
ROSA_CLARO = (255, 140, 140)
VERDE = (0, 255, 0)


# ==============================
# Configuraciones de las Celdas
# ==============================
tamanio_celda = TABLERO_ANCHO // 9


# ==============================
# Configuración de Fuentes
# ==============================
fuente_numeros = pygame.font.Font('fondo sudoku/PatrickHandSC-Regular.ttf', 40)
fuente_texto = pygame.font.SysFont('fondo sudoku/PatrickHandSC-Regular.ttf',27)


# ==============================
# Configuración de Botones
# ==============================
VALOR_BORDER_RADIUS = 20


# ==============================
# Inicialización de Variables
# ==============================
temporizador = 0
tablero = None
contador_errores = 0
celda_seleccionada = None
dificultad = "Facil"
ultimo_clic_dificultad = 0
cambio_anterior = False

# ==============================
# Variables para el pop-up
# ==============================

mostrar_popup = False
tiempo_inicio_popup = 0
duracion_popup = 2000  # Duración del pop-up en milisegundos (2 segundos)

# ==============================
# Variables para puntaje
# ==============================

puntaje_jugador = 0
PUNTOS_BASE = 1000
PENALIZACION_ERROR = 100
PENALIZACION_TIEMPO = 30
multiplicador_dificultad = None



# ==============================
# Configuración del Temporizador
# ==============================

pygame.time.set_timer(pygame.USEREVENT, 1000)  # Evento personalizado cada 1 segundo
DELAY_CLIC = 500  # 500 milisegundos de retraso entre clics


# ==============================
# Configuración de la Música
# ==============================
musica = pygame.mixer.Sound("fondo sudoku/musica_fondo.mp3") # se importa la musica de fondo de la carpeta de fondo sudoku
musica.set_volume(0.1) # se setea el volumen
pygame.time.set_timer(pygame.USEREVENT, 1000)  # Evento personalizado cada 1 segundo


# ==============================
# Cambiar el Estado entre Pantallas
# ==============================
corriendo = True
pantalla_actual = "menu" 



# ==============================
# Generación de Tablero y Sudoku
# ==============================

tablero_lleno = generar_tablero()
sudoku = generar_sudoku(tablero_lleno, "Facil")
matriz_booleana = generar_matriz_booleana(sudoku)
