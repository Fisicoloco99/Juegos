# ============================================================
# SCREENS.RPY - INTERFAZ GRÁFICA
# ============================================================

# --- CONFIGURACION DEL TABLERO ---
define COLUMNAS = 10
define FILAS = 10
define CASILLA_W = 80
define CASILLA_H = 80
define OFFSET_X = 560
define OFFSET_Y = 140

# --- PANTALLA DEL TABLERO ---
screen tablero_juego():
    modal True
    add Solid("#1a1a1a") # Fondo negro

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

    # 2. Salida (Arriba a la derecha)
    add Solid("#00FF00"):
        xpos OFFSET_X + 9 * CASILLA_W
        ypos OFFSET_Y + 0 * CASILLA_H
        xsize CASILLA_W
        ysize CASILLA_H
    text "SALIDA":
        xpos OFFSET_X + 9 * CASILLA_W
        ypos OFFSET_Y + 0 * CASILLA_H + 25
        xsize CASILLA_W
        text_align 0.5
        color "#000000"
        bold True

    # 3. Trampas (X rojas)
    for t in trampas:
        text "X":
            xpos OFFSET_X + t[0] * CASILLA_W + 25
            ypos OFFSET_Y + t[1] * CASILLA_H + 15
            size 40
            color "#FF0000"
            bold True

    # 4. Jugador (J azul)
    if jugador:
        text "J":
            xpos OFFSET_X + jugador.x * CASILLA_W + 25
            ypos OFFSET_Y + jugador.y * CASILLA_H + 15
            size 40
            color "#00AAFF"
            bold True

    # 5. Monstruo (M violeta)
    if monstruo:
        text "M":
            xpos OFFSET_X + monstruo.x * CASILLA_W + 25
            ypos OFFSET_Y + monstruo.y * CASILLA_H + 15
            size 40
            color "#FF00FF"
            bold True

    # 6. Panel de Mensajes
    frame:
        xpos 560
        ypos 30
        xsize 800
        background "#000000AA"
        padding (20, 10)
        text "[mensaje]" xalign 0.5 size 30 color "#FFFFFF"

# --- MENU PRINCIPAL ---
screen main_menu():
    tag menu
    add Solid("#0a0a1a")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20

        text "JUEGO DE ESCAPE" xalign 0.5 size 60 color "#ffffff" bold True
        null height 40

        textbutton "Comenzar" action Start() xalign 0.5 text_size 30
        textbutton "Cargar Partida" action ShowMenu("load") xalign 0.5 text_size 30
        textbutton "Opciones" action ShowMenu("preferences") xalign 0.5 text_size 30
        textbutton "Salir" action Quit(confirm=False) xalign 0.5 text_size 30

# --- MENU DE PAUSA ---
screen pause_menu():
    tag menu
    modal True
    add Solid("#000000CC")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 15

        text "PAUSA" xalign 0.5 size 50 color "#ffffff" bold True
        null height 20

        textbutton "Continuar" action Return() xalign 0.5 text_size 28
        textbutton "Guardar" action ShowMenu("save") xalign 0.5 text_size 28
        textbutton "Cargar" action ShowMenu("load") xalign 0.5 text_size 28
        textbutton "Menú Principal" action MainMenu() xalign 0.5 text_size 28
        textbutton "Salir del Juego" action Quit(confirm=True) xalign 0.5 text_size 28

# --- GUARDAR / CARGAR ---
screen save():
    tag menu
    add Solid("#0a0a1a")
    use file_slots("Guardar")
    textbutton "Volver" action Return() xalign 0.5 ypos 900 text_size 30

screen load():
    tag menu
    add Solid("#0a0a1a")
    use file_slots("Cargar")
    textbutton "Volver" action Return() xalign 0.5 ypos 900 text_size 30

screen file_slots(title):
    text title xalign 0.5 ypos 30 size 50 color "#ffffff" bold True

    grid 3 2:
        xalign 0.5
        yalign 0.45
        spacing 20

        for i in range(6):
            $ slot = i + 1
            button:
                xsize 350
                ysize 220
                background "#333333"
                hover_background "#555555"
                action FileAction(slot)
                has vbox
                add FileScreenshot(slot) xalign 0.5
                text FileTime(slot, format="%d/%m/%Y %H:%M", empty="Ranura vacía") xalign 0.5 color "#ffffff"
                text FileSaveName(slot) xalign 0.5 color "#cccccc"
                key "save_delete" action FileDelete(slot)

    hbox:
        xalign 0.5
        ypos 700
        spacing 10
        textbutton "<" action FilePagePrevious() text_size 24
        for page in range(1, 6):
            textbutton "[page]" action FilePage(page) text_size 24
        textbutton ">" action FilePageNext() text_size 24
