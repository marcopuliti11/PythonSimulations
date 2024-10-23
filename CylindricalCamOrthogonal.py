import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Cam parameters
cam_radius = 2  # base radius of the cam
amplitude = 1   # amplitude of the cam (how much the follower moves up and down)
frequency = 1   # angular frequency (rotation speed of the cam)
angular_velocity = 2 * np.pi * frequency  # angular velocity

# Simulation time
t_end = 10  # seconds
dt = 0.05   # time step
t = np.arange(0, t_end, dt)

# Calculate the follower's position
def follower_position(t):
    # Sinusoidal motion: height of the follower as a function of time
    return amplitude * np.sin(angular_velocity * t)

# Cam profile (a simple sinusoidal function around its perimeter)
theta = np.linspace(0, 2 * np.pi, 100)
cam_profile_x = (cam_radius + amplitude * np.sin(theta)) * np.cos(theta)
cam_profile_y = (cam_radius + amplitude * np.sin(theta)) * np.sin(theta)
cam_profile_z = np.zeros_like(theta)

# Arrays to store trajectory data
cam_trajectory_x = []
cam_trajectory_y = []
follower_trajectory_z = []

# Function to update the animation scene
def update(i, cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot):
    angle = angular_velocity * t[i]
    
    # Update cam position (rotating)
    cam_x = (cam_radius + follower_position(t[i])) * np.cos(angle)
    cam_y = (cam_radius + follower_position(t[i])) * np.sin(angle)
    
    # Update follower position (moving vertically)
    follower_z = follower_position(t[i])
    
    # Update cam plot
    cam.set_data([0, cam_x], [0, cam_y])
    cam.set_3d_properties([0, 0])
    
    # Update follower plot
    follower.set_data([0], [0])
    follower.set_3d_properties([follower_z])
    
    # Update the line connecting the cam to the follower
    follower_line.set_data([cam_x, 0], [cam_y, 0])
    follower_line.set_3d_properties([0, follower_z])
    
    # Store trajectory data
    cam_trajectory_x.append(cam_x)
    cam_trajectory_y.append(cam_y)
    follower_trajectory_z.append(follower_z)
    
    # Update trajectory plots in the second figure
    cam_traj_plot.set_data(cam_trajectory_x, cam_trajectory_y)
    follower_traj_plot.set_data(t[:i+1], follower_trajectory_z[:i+1])
    
    return cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot

# Create the figure and the 3D axis for the cam and follower animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize the cam and the follower
cam, = ax.plot([0, cam_radius], [0, 0], [0, 0], 'b', lw=2, label="Cam")
follower, = ax.plot([0], [0], [0], 'ro', markersize=10, label="Follower")
follower_line, = ax.plot([0, 0], [0, 0], [0, 0], 'g--', lw=2, label="Follower Line")

# Show the cam profile
cam_profile, = ax.plot(cam_profile_x, cam_profile_y, cam_profile_z, 'k--', lw=1, label="Cam Profile")

# Axis settings for the 3D plot
ax.set_xlim([-2.5, 2.5])
ax.set_ylim([-2.5, 2.5])
ax.set_zlim([-1.5, 1.5])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add the legend
ax.legend()

# Create a second figure for the 2D trajectory plots
fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

# Cam XY trajectory plot
cam_traj_plot, = ax1.plot([], [], 'b', lw=2)
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.5, 2.5)
ax1.set_xlabel('X (Cam)')
ax1.set_ylabel('Y (Cam)')
ax1.set_title('Cam XY Trajectory')

# Follower Z trajectory plot
follower_traj_plot, = ax2.plot([], [], 'r', lw=2)
ax2.set_xlim(0, t_end)
ax2.set_ylim(-amplitude, amplitude)
ax2.set_xlabel('Time')
ax2.set_ylabel('Z (Follower)')
ax2.set_title('Follower Z Trajectory')

# Create the animation
anim = FuncAnimation(fig, update, frames=len(t), fargs=(cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot), interval=50)

# Show both animations and trajectory plots
plt.show()
