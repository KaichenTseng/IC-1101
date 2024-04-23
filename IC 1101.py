import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define parameters
r_max = 10
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 100)
R, Theta = np.meshgrid(np.linspace(0, r_max, 100), theta)
Phi, _ = np.meshgrid(phi, np.linspace(0, 2 * np.pi, 100))

# Function to calculate gravitational potential
def gravitational_potential(r):
    return -1 / r

# Function to calculate gravitational force
def gravitational_force(r, mass):
    G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
    return G * mass / r**2  # Newton's law of universal gravitation

# Function to update plot
def update(num, ax, balls):
    ax.clear()
    # Define rotation angle
    angle = num * 0.1
    # Define Schwarzschild metric with rotation
    X = R * np.sin(Theta) * np.cos(Phi + angle)
    Y = R * np.sin(Theta) * np.sin(Phi + angle)
    Z = R * np.cos(Theta)
    # Plot the black holech
    ax.plot_surface(X, Y, Z, color='black', alpha=0.5)
    # Plot equipotential contours
    ax.contour(X, Y, gravitational_potential(R), 50, cmap='coolwarm')
    # Update balls
    for ball in balls:
        ball[0] -= 0.02 * ball[0]  # Move ball towards the center along X-axis (spiral inward)
        ball[1] -= 0.02 * ball[1]  # Move ball towards the center along Y-axis (spiral inward)
        ball[2] *= 1.01  # Stretch ball in Z-direction
        distance_to_center = np.sqrt(ball[0]**2 + ball[1]**2 + ball[2]**2)  # Distance to the center in meters
        gravitational_pull = gravitational_force(distance_to_center, 1)  # Assuming mass of 1 kg for each ball
        print(f"Ball at position {ball[:3]} experiences gravitational pull: {gravitational_pull:.2e} Newtons")
        if ball[2] > r_max:
            balls.remove(ball)
        else:
            ax.scatter(ball[0], ball[1], ball[2], color='red')  # Plot ball
    # Generate new ball every 5 seconds
    if num % 50 == 0:
        balls.append([r_max * np.cos(angle), r_max * np.sin(angle), 1])  # Spawn ball on circular trajectory

    # Set plot limits and labels
    ax.set_xlim([-r_max, r_max])
    ax.set_ylim([-r_max, r_max])
    ax.set_zlim([-r_max, r_max])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Trajectory and Force Visualization of IC 1101 by Ken')

# Create initial plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# List to store balls
balls = []

# Create animation
ani = FuncAnimation(fig, update, frames=range(1000), fargs=(ax, balls), interval=50)

# Show animation
plt.show()
