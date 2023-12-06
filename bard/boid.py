import pygame
import math
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
width, height = 800, 600  # Set the screen width and height

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def multiply(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def divide(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)


class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = 0

    def update(self, boids):
        # Cohesion
        cohesion_vector = Vector2D(0, 0)
        for boid in boids:
            cohesion_vector = cohesion_vector + Vector2D(boid.x, boid.y)
        cohesion_vector = cohesion_vector / len(boids)
        cohesion_vector = cohesion_vector - Vector2D(self.x, self.y)

        # Alignment
        align_vector = Vector2D()
        for boid in boids:
            if distance(self, boid) < 10:
                align_vector = align_vector + Vector2D(boid.direction)
        align_vector = align_vector / len(boids)

        # Separation
        separation_vector = Vector2D()
        for boid in boids:
            if distance(self, boid) < 5:
                separation_vector = separation_vector - Vector2D(boid.x, boid.y)
        separation_vector = separation_vector / len(boids)

        new_direction = self.direction + (cohesion_vector + align_vector + separation_vector) * 0.01
        new_direction = new_direction % 360

        new_x = self.x + self.speed * math.cos(new_direction)
        new_y = self.y + self.speed * math.sin(new_direction)

        if 0 <= new_x <= width and 0 <= new_y <= height:
            self.x = new_x
            self.y = new_y
            self.direction = new_direction

def draw_boid(screen, boid):
    pygame.draw.circle(screen, WHITE, (boid.x, boid.y), 5)

def distance(boid1, boid2):
    dx = boid2.x - boid1.x
    dy = boid2.y - boid1.y
    return magnitude(dx, dy)

def magnitude(dx, dy):
    return math.sqrt(dx * dx + dy * dy)

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Boids Simulation")

    boids = []
    for _ in range(100):
        boid = Boid(random.randint(10, width - 10), random.randint(10, height - 10))
        boids.append(boid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for boid in boids:
            draw_boid(screen, boid)
            boid.update(boids)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
