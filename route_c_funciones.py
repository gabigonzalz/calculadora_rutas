from queue import PriorityQueue


# Función para obtener coordenadas y comprobarlas
def obtener_coordenadas(tipo, tamano):
    coor = []
    for i in range(2):
        while True:
            coordenada = input(f"Ingrese la coordenada {i + 1} del {tipo} -> ")
            
            try:
                coordenada = int(coordenada)
                
                if 0 <= coordenada < tamano:
                    coor.append(coordenada)
                    break
                else:
                    print("El número ingresado no se encuentra dentro del mapa")
                    
            except ValueError:
                print("Lo ingresado no es un número, intentelo de nuevo.")
    return tuple(coor)


# Funcion para cambiar las coordenadas de inicio y de fin
def definir_coordenadas(tamano):
    print("Vamos a definir las coordenadas de inicio y de fin!")
    coor_inicio = obtener_coordenadas("inicio", tamano)
    coor_fin = obtener_coordenadas("fin", tamano)
    return coor_inicio, coor_fin


# Función para obtener elección
def obtener_eleccion(mensaje, opciones):
    while True:
        eleccion = input(mensaje)
        try:
            eleccion = int(eleccion)
            if eleccion in opciones:
                return eleccion
            else:
                print("El número ingresado no es una opción")
        except ValueError:
            print("Lo ingresado no es un número, intentelo de nuevo.")


# Función para definir obstáculos
def definir_obstaculos(mapa, tamano):
    print("Vamos a definir los obstáculos del mapa: ")
    opciones = [0, 1, 2, 3, 4]
    mensaje = """       Elija el tipo de obstáculo:
                    0 - Eliminar obstaculo
                    1 - Edificio
                    2 - Agua
                    3 - Bloqueo de ruta
                    4 - Atras
                    -> """
    while True:
        eleccion = obtener_eleccion(mensaje, opciones)
        if eleccion == 4:
            return mapa
        coordenadas = obtener_coordenadas("elemento",tamano)
        mapa[coordenadas[0]][coordenadas[1]] = eleccion


# Costo heurístico (distancia de Manhattan) entre dos celdas
def heur(celda1, celda2): # Costo H: pasos que necesito hacer
    return abs(celda1[0] - celda2[0]) + abs(celda1[1] - celda2[1])


# Función de movimientos válidos
def movimientos_validos(posicion, mapa, tamano):
    y, x = posicion
    movimientos = {}
    evitar_elementos = [1, 2, 3]
    if y > 0 and mapa[y - 1][x] not in evitar_elementos:
        movimientos["arriba"] = (y - 1, x)
    if y < tamano - 1 and mapa[y + 1][x] not in evitar_elementos:
        movimientos["abajo"] = (y + 1, x)
    if x > 0 and mapa[y][x - 1] not in evitar_elementos:
        movimientos["izquierda"] = (y, x - 1)
    if x < tamano - 1 and mapa[y][x + 1] not in evitar_elementos:
        movimientos["derecha"] = (y, x + 1)
    return movimientos


# Algoritmo A*
def aStar(mapa, coor_inicio, coor_fin):
    # Costo G: pasos que ya di
    costo_g = {tuple([y, x]): float('inf') for y in range(len(mapa)) for x in range(len(mapa[0]))}
    costo_g[coor_inicio] = 0
    # Valor F: costo G + Costo H
    valor_f = {tuple([y, x]): float('inf') for y in range(len(mapa)) for x in range(len(mapa[0]))}
    valor_f[coor_inicio] = heur(coor_inicio, coor_fin)
    
    a_revisar = PriorityQueue() # Cola a revisar
    a_revisar.put((valor_f[coor_inicio], coor_inicio))
    
    aCamino = {} # Lo revisado

    while not a_revisar.empty():
        # Agarramos la celda con menor valor F
        celdaActual = a_revisar.get()[1]
        
        if celdaActual == coor_fin:
            break
        
        # Obtenemos los movimientos válidos desde la celda actual
        direcciones = movimientos_validos(celdaActual, mapa, len(mapa))
        
        # Iteramos los movimientos validos
        for celdaHija in direcciones.values():
            temp_costo_g = costo_g[celdaActual] + 1 # Costo G de la hija +1 pq nos movimos
            temp_valor_f = temp_costo_g + heur(celdaHija, coor_fin) # Costo F de la hija
            
            # Si el nuevo valor F es mejor, actualizamos costos y metemos a la cola
            if temp_valor_f < valor_f[celdaHija]:
                costo_g[celdaHija] = temp_costo_g
                valor_f[celdaHija] = temp_valor_f
                a_revisar.put((temp_valor_f, celdaHija))
                
                # Marcamos el camino
                aCamino[celdaHija] = celdaActual

    # Si no se llego a la celda final retornar None
    if coor_fin not in aCamino:
        return None
    
    # Reconstruir el camino desde el final hasta el inicio
    aCaminoDerecho = {}
    celdaCamino = coor_fin
    while celdaCamino != coor_inicio:
        aCaminoDerecho[aCamino[celdaCamino]] = celdaCamino
        celdaCamino = aCamino[celdaCamino]
    return aCaminoDerecho


# Marcar el camino en el mapa
def CaminoAStar(mapa, coor_inicio, coor_fin):
    camino = aStar(mapa, coor_inicio, coor_fin)
    
    if camino is None:
        print("No se encontró un camino desde el inicio hasta el fin.")
        return mapa
    
    mapa_camino = [fila[:] for fila in mapa] # Slicing para evitar modificar el mapa original
    mapa_camino[coor_inicio[0]][coor_inicio[1]] = 9 # Marcamos el inicio
    for celda in camino.values(): # Llamamos a los valores del camino
        mapa_camino[celda[0]][celda[1]] = 9 # Marcamos el camino hasta el final
    return mapa_camino


# Función de imprimir el mapa y sus índices
def imprimir_mapa(mapa, tamano):
    mapeo = {0: '.', 1: 'X', 2: '@', 3: '!', 9: 'o'}
    
    # Crear una fila de índices para el borde superior
    fila_indices_superior = ['  '] + [str(i) for i in range(tamano)]
    mapa_visual = [fila_indices_superior]
    
    # Iterar sobre cada fila del mapa
    for i in range(tamano):
        # Añadir columna de indices para el borde izquierdo
        # Convertir la fila a una representación visual usando el diccionario de mapeo
        fila_visual = [str(i) + ' '] + [mapeo[elemento] for elemento in mapa[i]]
        mapa_visual.append(fila_visual)
        
    # Imprimir cada fila del mapa visual
    for fila in mapa_visual:
        print(' '.join(fila)) # Imprime como cadena unida por espacios
