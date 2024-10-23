import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Cam parameters
cam_radius = 1.0      # Reduced radius of the cylindrical cam in cm.
translation_stroke = 2.5  # Maximum vertical travel distance of the follower in cm (25 mm).
helix_turns = 1       # Number of helical turns along the height of the cam.
helix_pitch = translation_stroke / (2 * np.pi)  # Pitch of the helix, determines vertical rise per rotation.
cam_height = helix_turns * helix_pitch  # Total height of the cam based on the number of helical turns.
angular_velocity = 2 * np.pi / 10  # Angular velocity of the cam (in radians per second, simulates the rotation speed).

# Offset for the cam and follower along the X-axis
cam_offset_x = 0          # Cam's rotational axis X-offset (adjusts cam position in the X-direction).
follower_offset_x = 2.5    # Follower's translational axis X-offset (distance from cam axis, affects follower path).

# Simulation time
t_end = 10  # Total simulation time in seconds.
dt = 0.05   # Time step for each frame of the animation, impacts the smoothness of the motion.
t = np.arange(0, t_end, dt)  # Create an array of time values for the simulation.

# Calculate the follower's position based on the cam rotation
def follower_position(angle):
    # Determines the vertical position of the follower based on the cam's angle of rotation.
    if angle <= np.pi:  # First 180 degrees, follower remains at base (Z=0).
        return 0
    else:  # After 180 degrees, the follower moves according to the helical pitch.
        return helix_pitch * ((angle - np.pi) / (2 * np.pi))  # Linear motion along Z-axis based on rotation.

# Cam profile (helical groove traced around the cylinder's surface)
theta = np.linspace(0, 2 * np.pi * helix_turns, 1000)  # Generate angles for a complete helix.
cam_profile_x = cam_radius * np.cos(theta) + cam_offset_x  # X-coordinates based on radius and angle.
cam_profile_y = cam_radius * np.sin(theta)  # Y-coordinates for cam profile.

# Define Z coordinates: constant for the first 180 degrees, then increase
cam_profile_z = np.where(theta <= np.pi, 0, helix_pitch * ((theta - np.pi) / (2 * np.pi)))  # Z-coordinates for cam profile based on pitch.

# Arrays to store trajectory data
cam_trajectory_x = []  # List to store X positions of the cam over time.
cam_trajectory_y = []  # List to store Y positions of the cam over time.
follower_trajectory_z = []  # List to store Z positions of the follower over time.

# Function to create a cylinder for the follower
def create_cylinder(ax, x, y, z, radius, height):
    z = np.linspace(0, height, 100)  # Height of the cylinder (follower).
    theta = np.linspace(0, 2 * np.pi, 100)  # Angle for circular cross-section.
    theta_grid, z_grid = np.meshgrid(theta, z)  # Create a grid for the cylinder.
    x_grid = radius * np.cos(theta_grid) + x  # X-coordinates for the cylinder surface.
    y_grid = radius * np.sin(theta_grid) + y  # Y-coordinates for the cylinder surface.
    return ax.plot_surface(x_grid, y_grid, z_grid, color='r', alpha=0.5)  # Visual representation of the follower.

# Function to update the animation scene
def update(i, cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot, rod):
    angle = angular_velocity * t[i]  # Calculate the current angle of the cam based on time.

    # Update cam position (rotating in XY-plane, around Z-axis)
    cam_x = cam_radius * np.cos(angle) + cam_offset_x  # Update X position of cam.
    cam_y = cam_radius * np.sin(angle)  # Update Y position of cam.

    # Determine Z position of the cam and follower
    cam_z = 0  # Cam's Z remains at 0 for first 180 degrees.
    follower_z = follower_position(angle)  # Update follower position based on cam rotation.

    # Create rod from the follower position down to the base
    if i == 0:  # Initialize rod only once for the first frame.
        rod.set_data([follower_offset_x, follower_offset_x], [0, 0])
        rod.set_3d_properties([follower_z, 0])
    else:  # Update the rod position for subsequent frames.
        rod.set_data([follower_offset_x, follower_offset_x], [0, 0])
        rod.set_3d_properties([follower_z, 0])
    
    # Update cam plot
    cam.set_data([0, cam_x], [0, cam_y])  # Update cam's plot data.
    cam.set_3d_properties([cam_z, cam_z])  # Maintain Z position.

    # Update follower plot (follower is offset in the X-axis)
    follower.set_data([follower_offset_x], [0])  # Update follower position.
    follower.set_3d_properties([follower_z])  # Update Z position of follower.
    
    # Update the line connecting the cam to the follower (parallel with X-axis offset)
    follower_line.set_data([cam_x, follower_offset_x], [cam_y, 0])  # Line between cam and follower.
    follower_line.set_3d_properties([cam_z, follower_z])  # Set Z properties for the line.
    
    # Store trajectory data
    cam_trajectory_x.append(cam_x)  # Append cam's X position.
    cam_trajectory_y.append(cam_y)  # Append cam's Y position.
    follower_trajectory_z.append(follower_z)  # Append follower's Z position.
    
    # Update trajectory plots in the second figure
    cam_traj_plot.set_data(cam_trajectory_x, cam_trajectory_y)  # Update cam trajectory plot.
    follower_traj_plot.set_data(t[:i+1], follower_trajectory_z[:i+1])  # Update follower trajectory plot.
    
    return cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot, rod

# Create the figure and the 3D axis for the cam and follower animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize the cam and the follower
cam, = ax.plot([0, cam_radius], [0, 0], [0, 0], 'b', lw=2, label="Cam")  # Cam line.
follower, = ax.plot([follower_offset_x], [0], [0], 'ro', markersize=10, label="Follower")  # Follower point.
follower_line, = ax.plot([0, follower_offset_x], [0, 0], [0, 0], 'g--', lw=2, label="Follower Line")  # Connecting line.

# Initialize the rod
rod, = ax.plot([], [], [], 'k', lw=2, label="Rod")  # Black rod connecting follower to base.

# Show the cam profile (helical groove)
cam_profile, = ax.plot(cam_profile_x, cam_profile_y, cam_profile_z, 'k--', lw=1, label="Helical Groove")  # Cam groove visualization.

# Axis settings for the 3D plot
ax.set_xlim([-2.5, 2.5 + follower_offset_x])  # Set X-axis limits.
ax.set_ylim([-2.5, 2.5])  # Set Y-axis limits.
ax.set_zlim([0, cam_height])  # Set Z-axis limits.
ax.set_xlabel('X')  # Label for X-axis.
ax.set_ylabel('Y')  # Label for Y-axis.
ax.set_zlabel('Z')  # Label for Z-axis.

# Add the legend
ax.legend()

# Create a second figure for the 2D trajectory plots
fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

# Cam XY trajectory plot
cam_traj_plot, = ax1.plot([], [], 'b', lw=2)  # Plot for cam's XY trajectory.
ax1.set_xlim(-2.5, 2.5)  # Set limits for X-axis.
ax1.set_ylim(-2.5, 2.5)  # Set limits for Y-axis.
ax1.set_xlabel('X (Cam)')  # Label for X-axis of trajectory plot.
ax1.set_ylabel('Y (Cam)')  # Label for Y-axis of trajectory plot.
ax1.set_title('Cam XY Trajectory')  # Title for trajectory plot.

# Follower Z trajectory plot
follower_traj_plot, = ax2.plot([], [], 'r', lw=2)  # Plot for follower's Z trajectory.
ax2.set_xlim(0, t_end)  # Set limits for time axis.
ax2.set_ylim(0, translation_stroke)  # Set limits for follower's Z axis.
ax2.set_xlabel('Time (s)')  # Label for time axis.
ax2.set_ylabel('Z (Follower in cm)')  # Label for follower's Z axis.
ax2.set_title('Follower Z Trajectory')  # Title for follower trajectory plot.

# Create the animation
anim = FuncAnimation(fig, update, frames=len(t), fargs=(cam, follower, follower_line, cam_profile, cam_traj_plot, follower_traj_plot, rod), interval=50)

# Show both animations and trajectory plots
plt.show()
