# ============================================================
# VARIABLES DEL TABLERO (10x10)
# ============================================================
define COLUMNAS = 10
define FILAS = 10
define CASILLA_W = 90
define CASILLA_H = 90
define OFFSET_X = 510
define OFFSET_Y = 90

# ============================================================
# FUNCION DE CLIC 
# ============================================================
init python:
    def click_casilla(x, y):
        renpy.notify("Tocaste la casilla: " + str(x) + ", " + str(y))

# ============================================================
# SCREEN: TABLERO 10x10
# ============================================================
screen tablero():
    modal True
    fixed:
        # Fondo de pantalla 
        add Solid("#1a1a1a")

        # Grilla de botones
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                button:
                    xpos OFFSET_X + columna * CASILLA_W
                    ypos OFFSET_Y + fila * CASILLA_H
                    xsize CASILLA_W
                    ysize CASILLA_H
                    background "#333333"
                    hover_background "#555555"
                    action Function(click_casilla, columna, fila)