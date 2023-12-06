# Let's import pygame and initialize it
import pygame
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Boids Simulation')

# Colors
background_color = (255, 255, 255)
boid_color = (0, 0, 0)

# Initialize boids
num_boids = 100
boids = {
    'position': np.random.rand(num_boids, 2) * np.array([width, height]),
    'velocity': (np.random.rand(num_boids, 2) - 0.5) * 10
}

# Boids' parameters
view_range = 10.0  # Range of view for each boid
min_distance = 10.0  # Minimum distance to maintain from other boids
max_speed = 2.0  # Maximum speed a boid can travel in a timestep

# Boids' behavior functions
def limit_speed(velocity):
    """Limit the speed of a boid."""
    speed = np.linalg.norm(velocity)
    if speed > max_speed:
        velocity = (velocity / speed) * max_speed
    return velocity

def apply_rules(positions, velocities):
    """Apply the boids rules: separation, alignment, and cohesion."""
    new_velocities = np.copy(velocities)
    for i in range(num_boids):
        # Get the positions and velocities of the other boids
        others = np.delete(positions, i, axis=0)
        other_velocities = np.delete(velocities, i, axis=0)
        
        # Separation: steer to avoid crowding local flockmates
        differences = positions[i] - others
        distances = np.linalg.norm(differences, axis=1)
        close_boids = differences[distances < view_range, :]
        if close_boids.any():
            new_velocities[i] -= np.mean(close_boids, axis=0)

        # Alignment: steer towards the average heading of local flockmates
        local_velocities = other_velocities[distances < view_range, :]
        if local_velocities.any():
            new_velocities[i] += np.mean(local_velocities, axis=0) - velocities[i]

        # Cohesion: steer to move toward the average position of local flockmates
        local_positions = others[distances < view_range, :]
        if local_positions.any():
            new_velocities[i] += np.mean(local_positions, axis=0) - positions[i]

        # Apply the speed limit
        new_velocities[i] = limit_speed(new_velocities[i])
    return new_velocities

def update_boids(boids):
    positions = boids['position']
    velocities = boids['velocity']
    new_velocities = apply_rules(positions, velocities)
    boids['position'] += new_velocities
    # Boundary conditions - wrap around the screen
    boids['position'] %= np.array([width, height])

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update boids
    update_boids(boids)

    # Draw
    screen.fill(background_color)
    for position in boids['position']:
        pygame.draw.circle(screen, boid_color, position.astype(int), 2)

    # Refresh screen
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
sys.exit()
