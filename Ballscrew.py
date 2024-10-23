import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Ball screw parameters
screw_radius = 0.5      # Radius of the ball screw in cm
screw_pitch = 2.5        # Pitch of the ball screw in cm (vertical movement per full rotation)
screw_turns = 2         # Number of turns of the ball screw along its length
screw_height = screw_turns * screw_pitch  # Total height of the screw based on the number of turns
angular_velocity = 2 * np.pi / 10  # Angular velocity of the screw (rotations per second)

# Offset for the screw and follower along the X-axis
screw_offset_x = 0      # Screw's rotational axis X-offset
follower_offset_x = 2.5  # Follower's translational axis X-offset (parallel to the screw axis)

# Simulation time
t_end = 10  # seconds
dt = 0.05   # time step
t = np.arange(0, t_end, dt)

# Calculate the follower's position based on the screw rotation
def follower_position(angle):
    # The follower moves up according to the screw pitch based on the angle of rotation
    return (screw_pitch * (angle / (2 * np.pi)))  # Linear motion along Z-axis

# Screw profile (helix traced around the cylinder's surface)
theta = np.linspace(0, 2 * np.pi * screw_turns, 1000)  # Generate a helical path for the screw
screw_profile_x = screw_radius * np.cos(theta) + screw_offset_x
screw_profile_y = screw_radius * np.sin(theta)

# Define Z coordinates based on the screw pitch
screw_profile_z = screw_pitch * (theta / (2 * np.pi))  # Z-coordinates increase linearly with rotation

# Arrays to store trajectory data
screw_trajectory_x = []  # X positions of the screw over time
screw_trajectory_y = []  # Y positions of the screw over time
follower_trajectory_z = []  # Z positions of the follower over time

# Function to create a cylinder for the follower
def create_cylinder(ax, x, y, z, radius, height):
    z = np.linspace(0, height, 100)  # Height of the cylinder
    theta = np.linspace(0, 2 * np.pi, 100)  # Angle for circular cross-section
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid) + x
    y_grid = radius * np.sin(theta_grid) + y
    return ax.plot_surface(x_grid, y_grid, z_grid, color='r', alpha=0.5)  # Red cylinder for the follower

# Function to update the animation scene
def update(i, screw, follower, follower_line, screw_profile, screw_traj_plot, follower_traj_plot, rod):
    angle = angular_velocity * t[i]
    
    # Update screw position (rotating in XY-plane, around Z-axis)
    screw_x = screw_radius * np.cos(angle) + screw_offset_x
    screw_y = screw_radius * np.sin(angle)

    # Determine Z position of the screw and follower
    screw_z = follower_position(angle)  # Follower moves up according to screw rotation

    # Create rod from the follower position down to the base
    if i == 0:  # Initialize rod only once
        rod.set_data([follower_offset_x, follower_offset_x], [0, 0])
        rod.set_3d_properties([screw_z, 0])
    else:  # Update the rod position
        rod.set_data([follower_offset_x, follower_offset_x], [0, 0])
        rod.set_3d_properties([screw_z, 0])
    
    # Update screw plot
    screw.set_data([0, screw_x], [0, screw_y])
    screw.set_3d_properties([screw_z, screw_z])
    
    # Update follower plot (follower is offset in the X-axis)
    follower.set_data([follower_offset_x], [0])
    follower.set_3d_properties([screw_z])
    
    # Update the line connecting the screw to the follower (parallel with X-axis offset)
    follower_line.set_data([screw_x, follower_offset_x], [screw_y, 0])
    follower_line.set_3d_properties([screw_z, screw_z])
    
    # Store trajectory data
    screw_trajectory_x.append(screw_x)
    screw_trajectory_y.append(screw_y)
    follower_trajectory_z.append(screw_z)
    
    # Update trajectory plots in the second figure
    screw_traj_plot.set_data(screw_trajectory_x, screw_trajectory_y)
    follower_traj_plot.set_data(t[:i+1], follower_trajectory_z[:i+1])
    
    return screw, follower, follower_line, screw_profile, screw_traj_plot, follower_traj_plot, rod

# Create the figure and the 3D axis for the screw and follower animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize the screw and the follower
screw, = ax.plot([0, screw_radius], [0, 0], [0, 0], 'b', lw=2, label="Ball Screw")
follower, = ax.plot([follower_offset_x], [0], [0], 'ro', markersize=10, label="Nut")
follower_line, = ax.plot([0, follower_offset_x], [0, 0], [0, 0], 'g--', lw=2, label="Nut Line")

# Initialize the rod
rod, = ax.plot([], [], [], 'k', lw=2, label="Rod")  # Black rod

# Show the screw profile (helical groove)
screw_profile, = ax.plot(screw_profile_x, screw_profile_y, screw_profile_z, 'k--', lw=1, label="Helical Screw Groove")

# Axis settings for the 3D plot
ax.set_xlim([-2.5, 2.5 + follower_offset_x])
ax.set_ylim([-2.5, 2.5])
ax.set_zlim([0, screw_height])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add the legend
ax.legend()

# Create a second figure for the 2D trajectory plots
fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

# Screw XY trajectory plot
screw_traj_plot, = ax1.plot([], [], 'b', lw=2)
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.5, 2.5)
ax1.set_xlabel('X (Screw)')
ax1.set_ylabel('Y (Screw)')
ax1.set_title('Screw XY Trajectory')

# Follower Z trajectory plot
follower_traj_plot, = ax2.plot([], [], 'r', lw=2)
ax2.set_xlim(0, t_end)
ax2.set_ylim(0, screw_height)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Z (Nut in cm)')
ax2.set_title('Follower Z Trajectory')

# Create the animation
anim = FuncAnimation(fig, update, frames=len(t), fargs=(screw, follower, follower_line, screw_profile, screw_traj_plot, follower_traj_plot, rod), interval=50)

# Show both animations and trajectory plots
plt.show()
