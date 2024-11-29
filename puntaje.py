import json
from biblioteca import *

def crear_archivo(nombre_archivo) -> None:
    """
    Crea un archivo JSON vacío si no existe. Si el archivo ya existe, muestra un mensaje indicando que el archivo ya está creado.

    Parámetros:
        nombre_archivo (str): El nombre del archivo JSON que se desea crear.

    Retorno:
        None: No devuelve ningún valor. Si el archivo se crea correctamente, se inicializa con una lista vacía.
    
    Excepciones:
        FileExistsError: Si el archivo ya existe, se muestra un mensaje indicando que no se puede crear nuevamente.
    """
    try:
        with open(nombre_archivo, 'x') as archivo: #la 'x' abre un archivo para escritura solo si no existe.
            json.dump([], archivo) #crea lista vacia
    except FileExistsError: #si el archivo existe, tira "FileExistsError", por eso esta linea.
        print(f"El archivo {nombre_archivo} ya existe.")


def guardar_jugador(nombre_archivo, nombre_jugador, puntaje_jugador):
    """
    Guarda el puntaje de un jugador en un archivo JSON. Si el jugador ya existe, actualiza su puntaje si es mayor que el anterior.
    Además, ordena los puntajes en orden descendente y guarda solo los 5 mejores puntajes en el archivo.

    Parámetros:
        nombre_archivo (str): El nombre del archivo JSON donde se guardarán los puntajes.
        nombre_jugador (str): El nombre del jugador cuyo puntaje se desea guardar o actualizar.
        puntaje_jugador (int): El puntaje del jugador a guardar o actualizar.

    Retorno:
        None: La función no devuelve ningún valor. Los datos se guardan directamente en el archivo JSON especificado.

    Excepciones:
        FileNotFoundError: Si el archivo no existe, se crea un archivo vacío.
        json.JSONDecodeError: Si el archivo existe pero no es un archivo JSON válido, se maneja la excepción y se crea una lista vacía.
    
    Funcionalidad:
        - Si el jugador ya existe, se actualiza su puntaje solo si el nuevo puntaje es mayor que el anterior.
        - Si el jugador no existe, se agrega un nuevo registro con su nombre y puntaje.
        - Luego, los puntajes se ordenan en orden descendente usando el algoritmo de Bubble Sort.
        - Finalmente, se guardan solo los 5 mejores puntajes en el archivo, eliminando los puntajes inferiores.
    """
    try:
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)  # Cargar los datos existentes
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []  # Crear una lista vacía si el archivo no existe o está vacío

    #Actualiza el puntaje solo si es el mismo nombre
    jugador_existente = False
    for jugador in datos:
        if jugador["nombre"] == nombre_jugador: #si el jugador ya existe
            if puntaje_jugador > jugador["puntaje"]:  # Comparar puntajes
                jugador["puntaje"] = puntaje_jugador  # Actualizar al nuevo puntaje si es mayor
            jugador_existente = True
            break

    if not jugador_existente:
        # Si no existe, se agrega un nuevo jugador
        datos.append({"nombre": nombre_jugador, "puntaje": puntaje_jugador})

    #Ordenamiento descendente
    for i in range(len(datos) - 1):
        for j in range(i + 1, len(datos)):
            if datos[i]["puntaje"] < datos[j]["puntaje"]:
                aux = datos[i]
                datos[i] = datos[j]
                datos[j] = aux

    # Mantener solo los 5 mejores puntajes
    #datos = datos[:5]

    # Guardar los datos actualizados
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

        

def mostrar_archivo(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
            if not datos:
                print("No hay jugadores registrados.")
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe.")
    
    return datos  # Devuelve la lista vacía o los datos cargados, según corresponda

crear_archivo("nombre_ganadores.json")





