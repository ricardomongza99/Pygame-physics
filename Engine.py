import pygame
import random
import math

WIDTH, HEIGHT = 800, 800
NUMBER_OF_PARTICLES = 3

GRAVITY = (math.pi, 0.8)
# the loss of speed particles experience as they move through the air - the faster a particle is moving, the more speed is lost.
DRAG = 0.999
# the loss of speed a particle experiences when it hits a boundary.
ELASTICTY = 0.75

#COLROS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Particle():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = BLACK
        self.thickness = 2
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.angle, self.speed = addVectors(self.angle, self.speed, GRAVITY[0], GRAVITY[1])
        self.speed *= DRAG
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > WIDTH - self.size:
            # see how far it exceeded window
            self.x = 2 * (WIDTH - self.size) - self.x
            self.angle = -self.angle
            self.speed *= ELASTICTY

        if self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle
            self.speed *= ELASTICTY


        if self.y > HEIGHT - self.size:
            self.y = 2 * (HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= ELASTICTY


        if self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= ELASTICTY



def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy)
    if distance <= p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent


        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle

        # exchange their energy with one another
        p1.speed, p2.speed = p2.speed, p1.speed

        # reduce energy
        p1.speed *= ELASTICTY
        p2.speed *= ELASTICTY

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Test")
screen.fill(WHITE)

pygame.display.flip()

my_particles = []
my_particle = Particle(200, 200, 50)

for i in range(NUMBER_OF_PARTICLES):
    size = random.randint(50, 80)
    x = random.randint(0, WIDTH)
    y = random.randint(0, 50)

    particle = Particle(x, y, size)
    particle.speed = random.randint(1, 4)
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

selected_particle = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        if event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        # DRAGGING AROUND
        mouseX, mouseY = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = math.atan2(dy, dx) + 0.5 * math.pi
        selected_particle.speed = math.hypot(dx, dy) * 0.2

    screen.fill(WHITE)

    for i, particle in enumerate(my_particles):
        particle.bounce()
        particle.move()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()



    pygame.display.flip()
