import matplotlib.pyplot as plt
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
num_boids = 50
num_steps = 50
xlim = (0, 100)
ylim = (0, 100)

# Boids' initial positions and velocities
positions = np.random.uniform(low=min(xlim, ylim), high=max(xlim, ylim), size=(num_boids, 2))
velocities = np.random.uniform(-1, 1, size=(num_boids, 2))

# Boids' parameters
view_range = 10.0  # Range of view for each boid
min_distance = 2.0  # Minimum distance to maintain from other boids
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

# Simulation loop
for _ in range(num_steps):
    velocities = apply_rules(positions, velocities)
    positions += velocities

# Plot the final positions of the boids
plt.figure(figsize=(10, 8))
plt.scatter(positions[:, 0], positions[:, 1])
plt.xlim(xlim)
plt.ylim(ylim)
plt.title("Boids Simulation")
plt.xlabel("X position")
plt.ylabel("Y position")
plt.show()
