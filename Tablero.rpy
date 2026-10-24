# Constantes para el tablero
define COLUMNAS = 10
define FILAS = 10
define CASILLA_W = 80
define CASILLA_H = 80
define OFFSET_X = 560
define OFFSET_Y = 140

screen tablero_juego():
    modal True
    
    # Fondo
    add Solid("#1a1a1a")

    # 1. Grilla de botones
    for y in range(FILAS):
        for x in range(COLUMNAS):
            button:
                xpos OFFSET_X + x * CASILLA_W
                ypos OFFSET_Y + y * CASILLA_H
                xsize CASILLA_W
                ysize CASILLA_H
                background "#333333"
                hover_background "#555555"
                action Function(mover_jugador, x, y)

    # 2. Dibujar Salida (Arriba a la derecha)
    add Solid("#00FF00"):
        xpos OFFSET_X + 9 * CASILLA_W
        ypos OFFSET_Y + 0 * CASILLA_H
        xsize CASILLA_W
        ysize CASILLA_H
    text "SALIDA":
        xpos OFFSET_X + 9 * CASILLA_W
        ypos OFFSET_Y + 0 * CASILLA_H + 30
        xsize CASILLA_W
        text_align 0.5
        color "#000000"

    # 3. Dibujar Trampas
    for t in trampas:
        text "X":
            xpos OFFSET_X + t[0] * CASILLA_W + 25
            ypos OFFSET_Y + t[1] * CASILLA_H + 15
            size 40
            color "#FF0000"

    # 4. Dibujar Jugador
    if jugador:
        text "J":
            xpos OFFSET_X + jugador.x * CASILLA_W + 25
            ypos OFFSET_Y + jugador.y * CASILLA_H + 15
            size 40
            color "#00AAFF"
            bold True

    # 5. Dibujar Monstruo
    if monstruo:
        text "M":
            xpos OFFSET_X + monstruo.x * CASILLA_W + 25
            ypos OFFSET_Y + monstruo.y * CASILLA_H + 15
            size 40
            color "#FF00FF"
            bold True
