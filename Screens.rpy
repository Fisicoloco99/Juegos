# ============================================================
# SCREENS.RPY - ESQUELETO LIMPIO
# ============================================================

init python:
    config.game_menu_action = ShowMenu("pause_menu")

# ============================================================
# MENU PRINCIPAL
# ============================================================
screen main_menu():
    tag menu

    # Fondo simple (cambiar por una imagen si quieren)
    add Solid("#0a0a1a")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20

        text "MI JUEGO TÁCTICO" xalign 0.5 size 60 color "#ffffff" bold True
        null height 40

        textbutton "Comenzar Partida":
            action Start()
            xalign 0.5
            text_size 30

        textbutton "Cargar Partida":
            action ShowMenu("load")
            xalign 0.5
            text_size 30

        textbutton "Opciones":
            action ShowMenu("preferences")
            xalign 0.5
            text_size 30

        textbutton "Créditos":
            action ShowMenu("creditos_animados")
            xalign 0.5
            text_size 30

        textbutton "Salir":
            action Quit(confirm=False)
            xalign 0.5
            text_size 30

# ============================================================
# MENU DE PAUSA (En el juego)
# ============================================================
screen pause_menu():
    tag menu
    modal True
    add Solid("#000000CC") # Fondo semitransparente

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 15

        text "PAUSA" xalign 0.5 size 50 color "#ffffff" bold True
        null height 20

        textbutton "Continuar":
            action Return()
            xalign 0.5
            text_size 28

        textbutton "Guardar":
            action ShowMenu("save")
            xalign 0.5
            text_size 28

        textbutton "Cargar":
            action ShowMenu("load")
            xalign 0.5
            text_size 28

        textbutton "Opciones":
            action ShowMenu("preferences")
            xalign 0.5
            text_size 28

        textbutton "MenU Principal":
            action MainMenu()
            xalign 0.5
            text_size 28

        textbutton "Salir del Juego":
            action Quit(confirm=True)
            xalign 0.5
            text_size 28

# ============================================================
# GUARDAR Y CARGAR (Sistema de Ranuras)
# ============================================================
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
        for page in range(1, 6): # Reducido a 5 páginas
            textbutton "[page]" action FilePage(page) text_size 24
        textbutton ">" action FilePageNext() text_size 24

# ============================================================
# MENU DE OPCIONES (Choice)
# ============================================================
screen choice(items):
    style_prefix "choice"
    zorder 20

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 15

        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    yalign 0.5
    spacing 15

style choice_button:
    xalign 0.5
    xminimum 720
    padding (32, 16)
    background Frame(Solid("#182536EE"), 12, 12)
    hover_background Frame(Solid("#315579F5"), 12, 12)

style choice_button_text:
    xalign 0.5
    size 30
    color "#F3F6FB"
    hover_color "#FFE19A"

# ============================================================
# CRÉDITOS (Placeholder)
# ============================================================
screen creditos_animados():
    tag menu
    modal True

    add Solid("#000000")

    vbox:
        xalign 0.5
        spacing 20
        at creditos_scroll

        text "NOMBRE DEL JUEGO" xalign 0.5 size 70 color "#ffcc00" bold True
        null height 100

        text "EQUIPO DE DESARROLLO" xalign 0.5 size 35 color "#ffffff"
        null height 30
        text "Programador 1" xalign 0.5 size 28 color "#cccccc"
        text "Programador 2" xalign 0.5 size 28 color "#cccccc"
        text "Diseñador" xalign 0.5 size 28 color "#cccccc"

        null height 200
        text "© 2024" xalign 0.5 size 20 color "#888888"
        null height 500

    textbutton "Volver al menU" xalign 0.98 yalign 0.98 text_size 24 text_color "#888888" text_hover_color "#ffffff" action Return()
    timer 20.0 action Return()

transform creditos_scroll:
    ypos 1.0
    linear 20.0 ypos -1.5

# ============================================================
# ESTILOS DE TEXTO (Grandes y Centrados)
# ============================================================

style say_dialogue:
    size 38
    line_spacing 8
    xalign 0.5
    text_align 0.5

style say_label:
    size 42
    bold True
    xalign 0.5
    text_align 0.5

style menu_label:
    size 34
    color "#ffff88"
    bold True
    xalign 0.5
    text_align 0.5

style say_thought:
    size 38
    xalign 0.5
    text_align 0.5

style notify_text:
    size 26
    xalign 0.5
    text_align 0.5

style button_text:
    size 30
    xalign 0.5
    text_align 0.5

style window:
    ysize 280
    background "#000000cc"
    padding (60, 30)
    xalign 0.5

style namebox:
    xsize 400
    padding (30, 10)
    xalign 0.5