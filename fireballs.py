import pygame
import math
import random
import sys

ORBIT_RADIUS = 70
FIREBALL_SIZE = 14
PARTICLES_PER_FRAME = 3
MAX_PARTICLES = 600
ORBIT_SPEED = 1.8


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
            return (max(r, 60), max(g, 10), 0)

    @property
    def alpha(self):
        return int(255 * self.t)


def glow_surface(radius, color):
    r = radius * 3
    surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    for i in range(r, 0, -1):
        a = int(40 * (1 - i / r))
        if a <= 0:
            continue
        pygame.draw.circle(surf, (*color, a), (r, r), i)
    return surf


def main():
    pygame.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = pygame.display.set_mode((W, H), pygame.NOFRAME)
    pygame.display.set_caption("Fireballs — ESC to exit")
    clock = pygame.time.Clock()

    particles = []
    angle = 0.0

    glow = glow_surface(FIREBALL_SIZE, (255, 120, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
            a = p.alpha
            if a <= 0:
                continue
            c = p.color
            s = int(p.size * 2)
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            pygame.draw.circle(surf, (c[0], c[1], c[2], a), (s // 2, s // 2), int(p.size))
            screen.blit(surf, (int(p.x - p.size), int(p.y - p.size)))

        for i in range(3):
            a = angle + i * (2 * math.pi / 3)
            fx = mx + math.cos(a) * ORBIT_RADIUS
            fy = my + math.sin(a) * ORBIT_RADIUS
            ix, iy = int(fx), int(fy)
            r = FIREBALL_SIZE * 3
            screen.blit(glow, (ix - r, iy - r))
            pygame.draw.circle(screen, (255, 255, 220), (ix, iy), FIREBALL_SIZE)
            pygame.draw.circle(screen, (255, 200, 50), (ix, iy), FIREBALL_SIZE - 2)
            pygame.draw.circle(screen, (255, 100, 0), (ix, iy), FIREBALL_SIZE - 5)

        pygame.display.flip()


if __name__ == "__main__":
    main()
