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

# Boids' behavior functions
def limit_vector(vector, max_length):
    """ Limit the magnitude of a 2D vector to max_length. """
    length = np.linalg.norm(vector)
    if length > max_length:
        return vector / length * max_length
    return vector

def apply_boid_rules(boids, view_range, min_distance, max_speed):
    positions = boids['position']
    velocities = boids['velocity']
    num_boids = positions.shape[0]

    # Initialize forces
    separation_force = np.zeros_like(positions)
    alignment_force = np.zeros_like(positions)
    cohesion_force = np.zeros_like(positions)

    for i in range(num_boids):
        for j in range(num_boids):
            if i != j:
                distance = np.linalg.norm(positions[j] - positions[i])
                direction = positions[i] - positions[j]

                # Separation
                if distance < min_distance:
                    separation_force[i] += direction / (distance**2 + 1e-5)

                # Alignment
                if distance < view_range:
                    alignment_force[i] += velocities[j]

                # Cohesion
                if distance < view_range and distance > min_distance:
                    cohesion_force[i] += (positions[j] - positions[i]) / (distance + 1e-5)

    # Combine the forces with weights
    separation_force = limit_vector(separation_force, max_speed)
    alignment_force = limit_vector(alignment_force / (num_boids - 1), max_speed / 8)
    cohesion_force = limit_vector(cohesion_force / (num_boids - 1), max_speed / 100)

    # Apply the forces to velocities
    new_velocities = velocities + separation_force + alignment_force + cohesion_force

    # Limit the speed
    new_velocities = np.array([limit_vector(velocity, max_speed) for velocity in new_velocities])

    return new_velocities

# Adjust the parameters if necessary
view_range = 30.0  # View range for alignment and cohesion
min_distance = 20.0  # Minimum distance for separation
max_speed = 10.0  # Maximum speed for boid velocity

# Now you can call the apply_boid_rules function in your update loop to modify the velocities based on the rules.
# For example:
# boids['velocity'] = apply_boid_rules(boids, view_range, min_distance, max_speed)
# boids['position'] += boids['velocity']
# Ensure to include boundary checks so that boids wrap around or bounce back at the edges.

def update_boids(boids):
    positions = boids['position']
    velocities = boids['velocity']
    new_velocities = apply_boid_rules(boids, view_range, min_distance, max_speed)
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
