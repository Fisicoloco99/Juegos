# ============================================================
# SCRIPT.RPY - JUEGO COMPLETO TOP-DOWN (VISTA DESDE ARRIBA)
# ============================================================

# --- 1. DEFINICIÓN DE VARIABLES Y FUNCIONES BASE ---
init python:
    import math

    # Configuración de la vista Top-Down (Cuadrícula normal)
    TILE_SIZE = 50       # Tamaño de cada casilla en píxeles
    WORLD_W = 20         # Ancho del tablero en casillas
    WORLD_H = 20         # Alto del tablero en casillas
    OFFSET_X = 460       # Centrado en pantalla (1920x1080)
    OFFSET_Y = 40

    def grid_to_screen(wx, wy):
        """Convierte coordenadas del tablero a píxeles en pantalla."""
        sx = OFFSET_X + (wx * TILE_SIZE)
        sy = OFFSET_Y + (wy * TILE_SIZE)
        return (sx, sy)

    def screen_to_grid(sx, sy):
        """Convierte la posición del mouse en píxeles a coordenadas del tablero."""
        wx = (sx - OFFSET_X) / TILE_SIZE
        wy = (sy - OFFSET_Y) / TILE_SIZE
        return (wx, wy)

    def _circle(canvas, color, cx, cy, r, segments=18):
        """Dibuja un círculo aproximado usando un polígono."""
        pts = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        canvas.polygon(color, pts)

    # --- LÓGICA DEL JUEGO ---
    class TopDownGame:
        def __init__(self):
            self.reset()

        def reset(self):
            self.a_pos = [1.0, 10.0]  # Inicio de A
            self.b_pos = [18.0, 10.0] # Meta B
            self.lives = 5
            self.state = "playing"
            self.speed = 7.0          # Velocidad de A
            self.a_hit_r = 0.4        # Radio de colisión de A
            self.mine_hit_r = 0.4     # Radio de colisión de mina
            self.hit_invuln = 0.0
            self.explosions = []
            
            # Posiciones de las minas
            self.mines = [
                [4.5, 4.0], [6.0, 12.0], [3.0, 16.5], [8.5, 2.5],
                [10.0, 8.0], [12.5, 15.0], [14.0, 3.5], [7.0, 18.0],
                [15.5, 9.0], [16.5, 17.0], [11.0, 14.0], [2.0, 7.0],
                [9.5, 12.0], [5.5, 9.5], [13.5, 12.0], [17.0, 5.0],
                [12.0, 5.5], [4.0, 13.0], [9.0, 17.0], [15.0, 1.5],
                [6.5, 6.5], [11.5, 2.5], [8.0, 9.5], [14.5, 14.5],
            ]
            self.mines_alive = [True] * len(self.mines)

        def update(self, dt):
            if self.state != "playing":
                self._update_explosions(dt)
                return

            # 1. Obtener posición del mouse y convertirla a coordenadas del tablero
            mx, my = renpy.get_mouse_pos()
            mwx, mwy = screen_to_grid(mx, my)

            # Limitar el mouse a los bordes del tablero
            mwx = max(0.0, min(WORLD_W - 1.0, mwx))
            mwy = max(0.0, min(WORLD_H - 1.0, mwy))

            # 2. Mover el cubo A hacia el mouse
            ax, ay = self.a_pos
            dx, dy = mwx - ax, mwy - ay
            dist = math.hypot(dx, dy)
            
            if dist > 0.01:
                step = min(self.speed * dt, dist)
                ax += dx / dist * step
                ay += dy / dist * step
                # Asegurar que A no se salga del tablero
                ax = max(0.0, min(WORLD_W - 1.0, ax))
                ay = max(0.0, min(WORLD_H - 1.0, ay))
                self.a_pos = [ax, ay]

            # Bajar tiempo de invulnerabilidad (parpadeo)
            if self.hit_invuln > 0:
                self.hit_invuln = max(0.0, self.hit_invuln - dt)

            # 3. Colisión con minas
            r2 = (self.a_hit_r + self.mine_hit_r) ** 2
            for i, m in enumerate(self.mines):
                if not self.mines_alive[i]:
                    continue
                ddx = m[0] - ax
                ddy = m[1] - ay
                if ddx * ddx + ddy * ddy < r2 and self.hit_invuln <= 0:
                    self.mines_alive[i] = False
                    self.lives -= 1
                    self.hit_invuln = 1.2
                    self.explosions.append([m[0], m[1], 0.6])
                    if self.lives <= 0:
                        self.state = "lost"
                        return

            # 4. Colisión con la meta B
            bx, by = self.b_pos
            if abs(ax - bx) < 0.7 and abs(ay - by) < 0.7:
                self.state = "won"
                return

            self._update_explosions(dt)

        def _update_explosions(self, dt):
            for e in self.explosions:
                e[2] -= dt
            self.explosions = [e for e in self.explosions if e[2] > 0]

    # --- DIBUJADO EN PANTALLA (DISPLAYABLE) ---
    class GameDisplayable(renpy.Displayable):
        def __init__(self, game, **kwargs):
            super().__init__(**kwargs)
            self.game = game
            self._last_st = None
            self.a_label = renpy.text.text.Text("A", size=30, color="#ffffff", bold=True)
            self.b_label = renpy.text.text.Text("B", size=30, color="#ffffff", bold=True)

        def render(self, width, height, st, at):
            # Calcular tiempo transcurrido para el movimiento
            if self._last_st is None:
                dt = 0.016
            else:
                dt = min(st - self._last_st, 0.05)
            self._last_st = st

            self.game.update(dt)
            g = self.game

            # Pedir redibujado continuo (~60 FPS) si se está jugando
            if g.state == "playing" or g.explosions:
                renpy.redraw(self, 0.016)

            # Crear superficie de dibujo
            rv = renpy.Render(width, height)
            canvas = rv.canvas()
            canvas.rect("#0a0f18", (0, 0, width, height)) # Fondo general

            # 1. Dibujar la cuadrícula del tablero
            for x in range(WORLD_W + 1):
                sx, sy = grid_to_screen(x, 0)
                canvas.line("#1e2e45", (sx, sy), (sx, sy + WORLD_H * TILE_SIZE), 1)
            for y in range(WORLD_H + 1):
                sx, sy = grid_to_screen(0, y)
                canvas.line("#1e2e45", (sx, sy), (sx + WORLD_W * TILE_SIZE, sy), 1)

            # Borde del tablero
            top_left = grid_to_screen(0, 0)
            canvas.rect("#3a4a65", (top_left[0], top_left[1], WORLD_W * TILE_SIZE, WORLD_H * TILE_SIZE), 2)

            # 2. Dibujar las minas (que siguen vivas)
            for i, m in enumerate(g.mines):
                if g.mines_alive[i]:
                    self._draw_mine(canvas, m[0], m[1])

            # 3. Dibujar la Meta B
            self._draw_square(canvas, rv, g.b_pos[0], g.b_pos[1], "#00ff66", "#008833", self.b_label, width, height, st, at)

            # 4. Dibujar al Jugador A
            if g.hit_invuln > 0 and int(st * 12) % 2 == 0:
                top, side = "#ffffff", "#bbbbbb" # Parpadeo
            else:
                top, side = "#4c9aff", "#2a6edc" # Color normal
            self._draw_square(canvas, rv, g.a_pos[0], g.a_pos[1], top, side, self.a_label, width, height, st, at)

            # 5. Dibujar explosiones
            for e in g.explosions:
                ex, ey, life = e
                progress = 1.0 - (life / 0.6)
                rpx = (0.4 + progress * 1.2) * TILE_SIZE
                alpha = max(0, int(200 * (1.0 - progress)))
                if alpha > 0:
                    sx, sy = grid_to_screen(ex, ey)
                    _circle(canvas, "#ffaa00%02x" % alpha, sx, sy, rpx)
                    _circle(canvas, "#ff6600%02x" % max(0, alpha - 60), sx, sy, rpx * 0.6)

            return rv

        def _draw_mine(self, canvas, wx, wy):
            sx, sy = grid_to_screen(wx, wy)
            # Zona de peligro (círculo rojo translúcido)
            _circle(canvas, "#ff000033", sx, sy, TILE_SIZE * 0.5)
            # Bomba
            _circle(canvas, "#661111", sx, sy, 12)
            _circle(canvas, "#ff2222", sx, sy, 9)
            _circle(canvas, "#ff8888", sx - 3, sy - 3, 3)

        def _draw_square(self, canvas, rv, wx, wy, top_c, side_c, label, width, height, st, at):
            """Dibuja un cuadrado con una pequeña sombra para dar relieve."""
            sx, sy = grid_to_screen(wx, wy)
            hw = TILE_SIZE * 0.4 # Mitad del ancho del cubo
            
            # Sombra (ligeramente desplazada)
            canvas.rect("#00000099", (sx - hw + 4, sy - hw + 4, hw*2, hw*2))
            # Cara lateral (relieve)
            canvas.rect(side_c, (sx - hw, sy - hw + 4, hw*2, hw*2))
            # Cara superior
            canvas.rect(top_c, (sx - hw, sy - hw, hw*2, hw*2))

            # Letra A o B
            lr = renpy.render(label, width, height, st, at)
            lw, lh = lr.get_size()
            rv.blit(lr, (int(sx - lw / 2), int(sy - lh / 2)))

    # Funciones de control de UI
    def sync_ui():
        if store._last_state != store.game_instance.state:
            store._last_state = store.game_instance.state
            renpy.restart_interaction()

    def restart_game():
        store.game_instance.reset()
        store._last_state = "playing"
        renpy.restart_interaction()


# --- VARIABLES GLOBALES ---
default game_instance = TopDownGame()
default _last_state = "playing"


# --- PANTALLA PRINCIPAL DEL JUEGO ---
screen topdown_game_screen():
    modal True
    add GameDisplayable(game_instance)

    # Vidas (Corazones)
    hbox:
        xpos 30
        ypos 20
        spacing 6
        for i in range(5):
            if i < game_instance.lives:
                text "♥" size 42 color "#ff3344" bold True
            else:
                text "♡" size 42 color "#445566"

    # Instrucciones
    text "Guía el cubo A (azul) hasta B (verde) con el mouse. ¡Evitá las minas rojas!":
        xalign 0.5
        ypos 20
        size 24
        color "#99aabb"
        bold True

    # Refresco de UI
    timer 0.1 repeat True action Function(sync_ui)

    # Pantalla de Victoria
    if game_instance.state == "won":
        frame:
            xalign 0.5
            yalign 0.5
            background "#001a00ee"
            padding (60, 45)
            vbox:
                spacing 20
                text "¡LLEGASTE A LA META!" xalign 0.5 size 64 color "#00ff66" bold True
                text "Llegaste a B con [game_instance.lives] vidas restantes." xalign 0.5 size 24 color "#aaffaa"
                textbutton "Jugar de nuevo" action Function(restart_game) xalign 0.5 text_size 28
                textbutton "Menú principal" action MainMenu() xalign 0.5 text_size 28

    # Pantalla de Derrota
    elif game_instance.state == "lost":
        frame:
            xalign 0.5
            yalign 0.5
            background "#1a0000ee"
            padding (60, 45)
            vbox:
                spacing 20
                text "GAME OVER" xalign 0.5 size 64 color "#ff3344" bold True
                text "Pisaste demasiadas minas." xalign 0.5 size 24 color "#ffaaaa"
                textbutton "Reintentar" action Function(restart_game) xalign 0.5 text_size 28
                textbutton "Menú principal" action MainMenu() xalign 0.5 text_size 28


# --- INICIO DEL JUEGO ---
label start:
    call screen topdown_game_screen
    return
