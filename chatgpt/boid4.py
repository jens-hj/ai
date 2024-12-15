import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Boids Simulation')

# Boid parameters
num_boids = 50
min_distance = 20  # Distance at which boids will start separating from each other
view_range = 100   # How far a boid can see around itself
max_speed = 4
max_force = 0.1

# Colors
background_color = (255, 255, 255)
boid_color = (0, 0, 0)

# Boids' positions and velocities
positions = np.random.rand(num_boids, 2) * np.array([screen_width, screen_height])
velocities = (np.random.rand(num_boids, 2) - 0.5) * max_speed

# Functions for the boid behavior
def limit(vector, max_value):
    """Limit the magnitude of the 2D vector to max_value."""
    magnitude = np.linalg.norm(vector)
    if magnitude > max_value:
        return (vector / magnitude) * max_value
    return vector

def apply_rules(positions, velocities):
    new_velocities = np.copy(velocities)
    for i in range(num_boids):
        # Compute separation, alignment, and cohesion vectors
        # ... (Include the logic from the previous apply_rules function)
        pass  # Replace this with the actual computation

    # Limit the velocities and update positions
    new_velocities = np.array([limit(v, max_speed) for v in new_velocities])
    new_positions = positions + new_velocities
    return new_positions, new_velocities

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update boid positions and velocities
    positions, velocities = apply_rules(positions, velocities)

    # Draw background
    screen.fill(background_color)

    # Draw boids
    for position in positions:
        pygame.draw.circle(screen, boid_color, position.astype(int), 2)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
