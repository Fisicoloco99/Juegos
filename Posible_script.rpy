# ============================================================
# SCRIPT.RPY - LOGICA DEL JUEGO
# ============================================================

# --- CLASES BASE ---
init python:
    import random

    class Jugador:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Monstruo:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def mover_hacia(self, obj_x, obj_y):
            # IA básica: se mueve 1 casilla acercandose al jugador
            if self.x < obj_x: self.x += 1
            elif self.x > obj_x: self.x -= 1
            elif self.y < obj_y: self.y += 1
            elif self.y > obj_y: self.y -= 1

# --- VARIABLES GLOBALES ---
default jugador = None
default monstruo = None
default trampas = []
default juego_terminado = False
default mensaje = "Encuentra la SALIDA (verde). Evita las X rojas."

# --- INICIO DEL JUEGO ---
label start:
    # Posiciones iniciales
    $ jugador = Jugador(0, 9)
    $ monstruo = Monstruo(9, 0)
    $ juego_terminado = False
    
    # Generar 10 trampas aleatorias
    $ trampas = []
    $ while len(trampas) < 10:
        $ tx = random.randint(0, 9)
        $ ty = random.randint(0, 9)
        # Evitar que caigan en el jugador, monstruo o salida
        $ if (tx, ty) != (0, 9) and (tx, ty) != (9, 0) and (tx, ty) != (9, 0):
            $ trampas.append((tx, ty))
            
    jump jugar_tablero

# --- LOGICA DE MOVIMIENTO ---
init python:
    def mover_jugador(nx, ny):
        global juego_terminado, mensaje
        
        if juego_terminado:
            return
            
        # Solo permitir movimiento a casillas adyacentes (distancia 1)
        if abs(jugador.x - nx) + abs(jugador.y - ny) == 1:
            jugador.x = nx
            jugador.y = ny
            
            # 1. Revisar si llego a la salida (9,0)
            if jugador.x == 9 and jugador.y == 0:
                juego_terminado = True
                renpy.jump("victoria")
                return
                
            # 2. Revisar si piso una trampa
            if (jugador.x, jugador.y) in trampas:
                juego_terminado = True
                renpy.jump("derrota_trampa")
                return
                
            # 3. Mover al monstruo
            monstruo.mover_hacia(jugador.x, jugador.y)
            
            # 4. Revisar si el monstruo atrapo al jugador
            if monstruo.x == jugador.x and monstruo.y == jugador.y:
                juego_terminado = True
                renpy.jump("derrota_monstruo")
                return
                
            mensaje = "¡El monstruo se acerca!"
        else:
            mensaje = "Solo puedes moverte 1 casilla."

# --- LABELS DE FINALES ---
label victoria:
    "¡Llegaste a la salida y escapaste del monstruo!"
    "¡GANASTE!"
    return

label derrota_trampa:
    "Pisaste una trampa. El monstruo te alcanza..."
    "GAME OVER"
    return

label derrota_monstruo:
    "El monstruo te atrapó..."
    "GAME OVER"
    return
