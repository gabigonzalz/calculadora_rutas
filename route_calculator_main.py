import route_c_funciones as rc


# Mapa predeterminado
mapa = [[0,0,0,0,0,0],
        [0,1,1,0,1,1],
        [0,1,1,0,1,1],
        [3,3,0,0,0,2],
        [2,2,2,2,0,2],
        [0,0,0,0,0,0],]

tamano = len(mapa)

# Coordenadas predeterminadas
coor_inicio = (0, 0)
coor_fin = (5, 5)

# --------------------------------Flujo principal----------------------------------

print("""
      BIENVENIDO A TU CALCULADOR DE RUTAS
      """)

rc.imprimir_mapa(mapa,tamano)

menu = 1
while menu!= 0:
    
    opciones = [0,1,2,3,4]
    mensaje = """
                    Elija una opcion:
                0 - Salir
                1 - Cambiar inicio y fin
                2 - Modificar obstaculos
                3 - Imprimir mapa
                4 - Encontrar camino
                -> """

    # Pedimos al usuario una opcion
    menu = rc.obtener_eleccion(mensaje,opciones)
    
    # Cambiar coordenadas de inicio y de fin
    if menu == 1:
        coor_inicio,coor_fin = rc.definir_coordenadas(tamano)
        
    # Anadir obstaculos 
    elif menu == 2:
        mapa = rc.definir_obstaculos(mapa,tamano)
    
    # Imprimir mapa
    elif menu == 3:
        rc.imprimir_mapa(mapa,tamano)
        
    # Encontrar camino
    elif menu == 4:
        mapa_resultado = rc.CaminoAStar(mapa, coor_inicio, coor_fin)
        rc.imprimir_mapa(mapa_resultado, tamano)
        
        
print("    ")
print("Asi quedo tu ruta")
mapa_resultado = rc.CaminoAStar(mapa, coor_inicio, coor_fin)
rc.imprimir_mapa(mapa_resultado, tamano)

