# ============================================================
# SCRIPT.RPY - JUEGO COMPLETO 2.5D (CUBO A A CUBO B CON MOUSE)
# ============================================================

# --- 1. DEFINICIÓN DE VARIABLES Y FUNCIONES BASE ---
init python:
    import math

    # Configuración de la proyección isométrica (2.5D)
    ISO_TILE_W = 64
    ISO_TILE_H = 32
    ISO_OFFSET_X = 960.0
    ISO_OFFSET_Y = 260.0
    ISO_WORLD_W = 20
    ISO_WORLD_H = 20
    ISO_CUBE_H = 34

    def iso_to_screen(wx, wy):
        sx = ISO_OFFSET_X + (wx - wy) * ISO_TILE_W * 0.5
        sy = ISO_OFFSET_Y + (wx + wy) * ISO_TILE_H * 0.5
        return (sx, sy)

    def screen_to_iso(sx, sy):
        dx = sx - ISO_OFFSET_X
        dy = sy - ISO_OFFSET_Y
        wx = dx / ISO_TILE_W + dy / ISO_TILE_H
        wy = dy / ISO_TILE_H - dx / ISO_TILE_W
        return (wx, wy)

    def _circle(canvas, color, cx, cy, r, segments=18):
        pts = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        canvas.polygon(color, pts)

    def _iso_diamond(canvas, color, wx, wy, hw, hh):
        pts = [
            iso_to_screen(wx - hw, wy - hh),
            iso_to_screen(wx + hw, wy - hh),
            iso_to_screen(wx + hw, wy + hh),
            iso_to_screen(wx - hw, wy + hh),
        ]
        canvas.polygon(color, pts)

    # Clase principal que maneja la lógica del juego
    class IsoGame:
        def __init__(self):
            self.reset()

        def reset(self):
            self.a_pos = [1.0, 10.0] # Posición inicial de A
            self.b_pos = [18.0, 10.0] # Posición de B (Meta)
            self.lives = 5 # 5 vidas
            self.state = "playing" # "playing", "won", "lost"
            self.speed = 7.0 # Velocidad del cubo A
            self.a_hit_r = 0.35
            self.mine_hit_r = 0.30
            self.hit_invuln = 0.0
            self.explosions = []
            
            # Coordenadas de las minas (X, Y)
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

            # 1. El cubo A sigue al mouse
            mx, my = renpy.get_mouse_pos()
            mwx, mwy = screen_to_iso(mx, my)

            # Limitar el mouse a los bordes del tablero
            mwx = max(0.0, min(ISO_WORLD_W - 1.0, mwx))
            mwy = max(0.0, min(ISO_WORLD_H - 1.0, mwy))

            ax, ay = self.a_pos
            dx, dy = mwx - ax, mwy - ay
            dist = math.hypot(dx, dy)
            
            if dist > 0.01:
                step = min(self.speed * dt, dist)
                ax += dx / dist * step
                ay += dy / dist * step
                ax = max(0.0, min(ISO_WORLD_W - 1.0, ax))
                ay = max(0.0, min(ISO_WORLD_H - 1.0, ay))
                self.a_pos = [ax, ay]

            if self.hit_invuln > 0:
                self.hit_invuln = max(0.0, self.hit_invuln - dt)

            # 2. Colisiones con minas (pierde vida)
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

            # 3. ¿Llegó a B?
            bx, by = self.b_pos
            if abs(ax - bx) < 0.6 and abs(ay - by) < 0.6:
                self.state = "won"
                return

            self._update_explosions(dt)

        def _update_explosions(self, dt):
            for e in self.explosions:
                e[2] -= dt
            self.explosions = [e for e in self.explosions if e[2] > 0]

    # Clase que dibuja todo en pantalla
    class IsoDisplayable(renpy.Displayable):
        def __init__(self, game, **kwargs):
            super().__init__(**kwargs)
            self.game = game
            self._last_st = None
            self.a_label = renpy.text.text.Text("A", size=26, color="#ffffff", bold=True)
            self.b_label = renpy.text.text.Text("B", size=26, color="#ffffff", bold=True)

        def render(self, width, height, st, at):
            if self._last_st is None:
                dt = 0.016
            else:
                dt = min(st - self._last_st, 0.05)
            self._last_st = st

            self.game.update(dt)
            g = self.game

            if g.state == "playing" or g.explosions:
                renpy.redraw(self, 0.016)

            rv = renpy.Render(width, height)
            canvas = rv.canvas()
            canvas.rect("#0a0f18", (0, 0, width, height))

            # Dibujar Tablero
            big = [
                iso_to_screen(-0.5, -0.5),
                iso_to_screen(ISO_WORLD_W - 0.5, -0.5),
                iso_to_screen(ISO_WORLD_W - 0.5, ISO_WORLD_H - 0.5),
                iso_to_screen(-0.5, ISO_WORLD_H - 0.5),
            ]
            canvas.polygon("#152236", big)

            for k in range(ISO_WORLD_W + 1):
                canvas.line("#1e2e45", iso_to_screen(k - 0.5, -0.5), iso_to_screen(k - 0.5, ISO_WORLD_H - 0.5), 1)
            for k in range(ISO_WORLD_H + 1):
                canvas.line("#1e2e45", iso_to_screen(-0.5, k - 0.5), iso_to_screen(ISO_WORLD_W - 0.5, k - 0.5), 1)
            for i in range(4):
                canvas.line("#3a4a65", big[i], big[(i + 1) % 4], 2)

            # Ordenar por profundidad para el efecto 2.5D
            drawables = []
            for i, m in enumerate(g.mines):
                if g.mines_alive[i]:
                    drawables.append(("mine", m[0], m[1], i))
            drawables.append(("A", g.a_pos[0], g.a_pos[1], None))
            drawables.append(("B", g.b_pos[0], g.b_pos[1], None))
            drawables.sort(key=lambda t: t[1] + t[2])

            for kind, wx, wy, idx in drawables:
                if kind == "mine":
                    self._draw_mine(canvas, wx, wy)
                elif kind == "A":
                    if g.hit_invuln > 0 and int(st * 12) % 2 == 0:
                        top, lf, rt = "#ffffff", "#bbbbbb", "#dddddd"
                    else:
                        top, lf, rt = "#4c9aff", "#2a6edc", "#3a7ee8"
                    self._draw_cube(canvas, rv, wx, wy, top, lf, rt, self.a_label, width, height, st, at)
                elif kind == "B":
                    self._draw_cube(canvas, rv, wx, wy, "#00ff66", "#008833", "#00aa44", self.b_label, width, height, st, at)

            # Explosiones
            for e in g.explosions:
                ex, ey, life = e
                progress = 1.0 - (life / 0.6)
                rw = 0.3 + progress * 1.5
                rpx = rw * ISO_TILE_W * 0.5
                alpha = max(0, int(200 * (1.0 - progress)))
                if alpha > 0:
                    sx, sy = iso_to_screen(ex, ey)
                    cy = sy - ISO_CUBE_H * 0.4
                    _circle(canvas, "#ffaa00%02x" % alpha, sx, cy, rpx)
                    _circle(canvas, "#ff6600%02x" % max(0, alpha - 60), sx, cy, rpx * 0.6)

            return rv

        def _draw_mine(self, canvas, wx, wy):
            _iso_diamond(canvas, "#ff000022", wx, wy, 0.55, 0.55)
            _iso_diamond(canvas, "#3a0a0a", wx, wy, 0.4, 0.4)
            sx, sy = iso_to_screen(wx, wy)
            _circle(canvas, "#661111", sx, sy - 10, 11)
            _circle(canvas, "#ff2222", sx, sy - 14, 9)
            _circle(canvas, "#ff8888", sx - 3, sy - 17, 3)

        def _draw_cube(self, canvas, rv, wx, wy, top_c, left_c, right_c, label, width, height, st, at):
            sx, sy = iso_to_screen(wx, wy)
            hw = 0.5 * ISO_TILE_W * 0.5
            hh = 0.5 * ISO_TILE_H * 0.5
            ch = ISO_CUBE_H

            _iso_diamond(canvas, "#00000099", wx, wy, 0.55, 0.55)

            left = [(sx - hw, sy - ch), (sx, sy - ch + hh), (sx, sy + hh), (sx - hw, sy)]
            right = [(sx + hw, sy - ch), (sx, sy - ch + hh), (sx, sy + hh), (sx + hw, sy)]
            canvas.polygon(left_c, left)
            canvas.polygon(right_c, right)

            top = [(sx, sy - ch - hh), (sx + hw, sy - ch), (sx, sy - ch + hh), (sx - hw, sy - ch)]
            canvas.polygon(top_c, top)

            lr = renpy.render(label, width, height, st, at)
            lw, lh = lr.get_size()
            rv.blit(lr, (int(sx - lw / 2), int(sy - ch - lh / 2)))

    # Funciones para reiniciar y actualizar la pantalla
    def sync_iso_ui():
        if store._iso_last_state != store.mouse_game.state:
            store._iso_last_state = store.mouse_game.state
            renpy.restart_interaction()

    def restart_iso_game():
        store.mouse_game.reset()
        store._iso_last_state = "playing"
        renpy.restart_interaction()


# --- 2. INICIALIZACIÓN DE VARIABLES GLOBALES ---
default mouse_game = IsoGame()
default _iso_last_state = "playing"


# --- 3. PANTALLA PRINCIPAL DEL JUEGO ---
screen mouse_game_screen():
    modal True
    add IsoDisplayable(mouse_game)

    # Corazones (Vidas)
    hbox:
        xpos 30
        ypos 20
        spacing 6
        for i in range(5):
            if i < mouse_game.lives:
                text "♥" size 42 color "#ff3344" bold True
            else:
                text "♡" size 42 color "#445566"

    # Texto de ayuda
    text "Movés el mouse y el cubo A lo sigue. Llegá al cubo B (verde) sin tocar las minas rojas.":
        xalign 0.5
        ypos 60
        size 22
        color "#99aabb"

    timer 0.1 repeat True action Function(sync_iso_ui)

    # Pantalla de Victoria
    if mouse_game.state == "won":
        frame:
            xalign 0.5
            yalign 0.5
            background "#001a00ee"
            padding (60, 45)
            vbox:
                spacing 20
                text "¡ESCAPASTE!" xalign 0.5 size 64 color "#00ff66" bold True
                text "Llegaste a B con [mouse_game.lives] vidas." xalign 0.5 size 24 color "#aaffaa"
                textbutton "Jugar de nuevo" action Function(restart_iso_game) xalign 0.5 text_size 28
                textbutton "Menú principal" action MainMenu() xalign 0.5 text_size 28

    # Pantalla de Derrota
    elif mouse_game.state == "lost":
        frame:
            xalign 0.5
            yalign 0.5
            background "#1a0000ee"
            padding (60, 45)
            vbox:
                spacing 20
                text "GAME OVER" xalign 0.5 size 64 color "#ff3344" bold True
                text "Te quedaste sin vidas." xalign 0.5 size 24 color "#ffaaaa"
                textbutton "Reintentar" action Function(restart_iso_game) xalign 0.5 text_size 28
                textbutton "Menú principal" action MainMenu() xalign 0.5 text_size 28


# --- 4. INICIO DEL JUEGO ---
label start:
    call screen mouse_game_screen
    return