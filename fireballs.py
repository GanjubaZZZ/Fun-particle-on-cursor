import pygame
import math
import random
import sys
import ctypes

ORBIT_RADIUS = 70
FIREBALL_SIZE = 14
PARTICLES_PER_FRAME = 3
MAX_PARTICLES = 600
ORBIT_SPEED = 1.8

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
LWA_COLORKEY = 0x01
VK_ESCAPE = 0x1B


def make_window_transparent(hwnd):
    user32 = ctypes.windll.user32
    ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT)
    user32.SetLayeredWindowAttributes(hwnd, 0x000000, 0, LWA_COLORKEY)


class Particle:
    def __init__(self, x, y):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.5)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 0.8
        self.life = random.randint(20, 50)
        self.max_life = self.life
        self.size = random.uniform(2, 5.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.vy -= 0.06
        self.life -= 1

    @property
    def dead(self):
        return self.life <= 0

    @property
    def t(self):
        return max(0, self.life / self.max_life)

    @property
    def color(self):
        t = self.t
        if t > 0.7:
            g = int(255 * (t - 0.7) / 0.3)
            return (255, min(g, 255), 0)
        elif t > 0.35:
            g = int(180 * (t - 0.35) / 0.35)
            return (255, min(g, 180), 0)
        else:
            r = int(255 * t / 0.35)
            g = int(50 * t / 0.35)
            return (max(r, 20), max(g, 3), 0)


def make_glow():
    diam = FIREBALL_SIZE * 6
    surf = pygame.Surface((diam, diam))
    surf.set_colorkey((0, 0, 0))
    cx = cy = diam // 2
    max_r = FIREBALL_SIZE * 3
    for r in range(max_r, FIREBALL_SIZE, -1):
        t = (r - FIREBALL_SIZE) / (max_r - FIREBALL_SIZE)
        pygame.draw.circle(surf, (int(255 * t), int(120 * t), 0), (cx, cy), r)
    return surf


def main():
    pygame.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = pygame.display.set_mode((W, H), pygame.NOFRAME)
    pygame.display.set_caption("Fireballs — ESC to exit")
    clock = pygame.time.Clock()

    hwnd = pygame.display.get_wm_info()['window']
    make_window_transparent(hwnd)

    particles = []
    angle = 0.0
    glow = make_glow()

    while True:
        if ctypes.windll.user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60) / 1000.0
        mx, my = pygame.mouse.get_pos()
        angle += ORBIT_SPEED * dt

        for i in range(3):
            a = angle + i * (2 * math.pi / 3)
            fx = mx + math.cos(a) * ORBIT_RADIUS
            fy = my + math.sin(a) * ORBIT_RADIUS
            for _ in range(PARTICLES_PER_FRAME):
                particles.append(Particle(fx, fy))

        for p in particles:
            p.update()
        particles = [p for p in particles if not p.dead]
        if len(particles) > MAX_PARTICLES:
            particles = particles[-MAX_PARTICLES:]

        screen.fill((0, 0, 0))

        for p in particles:
            pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), int(p.size))

        for i in range(3):
            a = angle + i * (2 * math.pi / 3)
            fx = mx + math.cos(a) * ORBIT_RADIUS
            fy = my + math.sin(a) * ORBIT_RADIUS
            ix, iy = int(fx), int(fy)
            screen.blit(glow, (ix - FIREBALL_SIZE * 3, iy - FIREBALL_SIZE * 3))
            pygame.draw.circle(screen, (255, 255, 220), (ix, iy), FIREBALL_SIZE)
            pygame.draw.circle(screen, (255, 200, 50), (ix, iy), FIREBALL_SIZE - 2)
            pygame.draw.circle(screen, (255, 100, 0), (ix, iy), FIREBALL_SIZE - 5)

        pygame.display.flip()


if __name__ == "__main__":
    main()
