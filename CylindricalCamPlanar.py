import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Cam parameters
cam_radius = 2      # Radius of the cylindrical cam
helix_pitch = 1     # Pitch of the helical groove (distance between turns in the Z direction)
turns = 3           # Number of helical turns along the cam's height
cam_height = turns * helix_pitch  # Total height of the cam based on the number of turns
angular_velocity = 2 * np.pi / 5  # Angular velocity of the cam (rotations per second)

# Offset for the cam and follower along the X-axis
cam_offset_x = 0          # Cam's rotational axis X-offset
follower_offset_x = 3     # Follower's translational axis X-offset (parallel to the cam axis)

# Simulation time
t_end = 10  # seconds
dt = 0.05   # time step
t = np.arange(0, t_end, dt)

# Calculate the follower's position based on the cam rotation (Z-axis translation from helix)
def follower_position(angle):
    # Helicoidal motion: Z-position is a function of the angle (helix pitch)
    return helix_pitch * (angle / (2 * np.pi))  # Linear motion along Z-axis

# Cam profile (helical groove traced around the cylinder's surface)
theta = np.linspace(0, 2 * np.pi * turns, 1000)  # Generate a helix over the cam's surface
cam_profile_x = cam_radius * np.cos(theta) + cam_offset_x
cam_profile_y = cam_radius * np.sin(theta)
cam_profile_z = helix_pitch * theta / (2 * np.pi)  # Helix grows in Z-direction as theta increases

# Arrays to store trajectory data
cam_trajectory_x = []
cam_trajectory_y = []
follower_trajectory_z = []

# Function to update the animation scene
def update(i, cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot):
    angle = angular_velocity * t[i]
    
    # Update cam position (rotating in XY-plane, around Z-axis)
    cam_x = cam_radius * np.cos(angle) + cam_offset_x
    cam_y = cam_radius * np.sin(angle)
    cam_z = follower_position(angle)  # Z position as a function of cam angle (helicoidal)
    
    # Update follower position (moving along Z-axis based on the helical profile)
    follower_z = follower_position(angle)
    
    # Update cam plot
    cam.set_data([0, cam_x], [0, cam_y])
    cam.set_3d_properties([cam_z, cam_z])
    
    # Update follower plot (follower is offset in the X-axis)
    follower.set_data([follower_offset_x], [0])
    follower.set_3d_properties([follower_z])
    
    # Update the line connecting the cam to the follower (parallel with X-axis offset)
    follower_line.set_data([cam_x, follower_offset_x], [cam_y, 0])
    follower_line.set_3d_properties([cam_z, follower_z])
    
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
cam, = ax.plot([0, cam_radius], [0, 0], [cam_height/2, cam_height/2], 'b', lw=2, label="Cam")
follower, = ax.plot([follower_offset_x], [0], [0], 'ro', markersize=10, label="Follower")
follower_line, = ax.plot([0, follower_offset_x], [0, 0], [cam_height/2, 0], 'g--', lw=2, label="Follower Line")

# Show the cam profile (helical groove)
cam_profile, = ax.plot(cam_profile_x, cam_profile_y, cam_profile_z, 'k--', lw=1, label="Helical Groove")

# Axis settings for the 3D plot
ax.set_xlim([-2.5, 2.5 + follower_offset_x])
ax.set_ylim([-2.5, 2.5])
ax.set_zlim([0, cam_height])
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
ax2.set_ylim(0, cam_height)
ax2.set_xlabel('Time')
ax2.set_ylabel('Z (Follower)')
ax2.set_title('Follower Z Trajectory')

# Create the animation
anim = FuncAnimation(fig, update, frames=len(t), fargs=(cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot), interval=50)

# Show both animations and trajectory plots
plt.show()
