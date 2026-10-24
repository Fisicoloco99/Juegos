# ============================================================
# OPCIONES.RPY - ESTILOS Y CONFIGURACIÓN
# ============================================================

init python:
    config.game_menu_action = ShowMenu("pause_menu")

# --- ESTILOS DE TEXTO ---
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

style choice_button_text:
    size 30
    xalign 0.5
    text_align 0.5

style window:
    ysize 280
    background "#000000cc"
    padding (60, 30)
    xalign 0.5
