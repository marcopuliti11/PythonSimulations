import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define the linkage parameters
linkage_length_A = 1.0  # Length of Linkage A
linkage_length_B = 1.0  # Length of Linkage B

# Create the figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize lines for linkages
line_A, = ax.plot([], [], [], lw=3, color='blue', label='Linkage A (Flex/Ext)')
line_B, = ax.plot([], [], [], lw=3, color='orange', label='Linkage B (Ab/Ad)')

# Set the limits and labels
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('X (Flex/Ext)')
ax.set_ylabel('Y (Ab/Ad)')
ax.set_zlabel('Z (Motor)')
ax.set_title('3D Orthogonal Linkage System')
ax.view_init(elev=20, azim=30)  # Initial viewing angle

# Function to initialize the plot
def init():
    line_A.set_data([], [])
    line_A.set_3d_properties([])
    line_B.set_data([], [])
    line_B.set_3d_properties([])
    return line_A, line_B,

# Update function for animation
def update(frame):
    # Calculate the angles for the two linkages
    theta_A = np.radians(frame)  # Angle for Linkage A (Flex/Ext)
    theta_B = np.radians(frame * 1.5)  # Angle for Linkage B (Ab/Ad)
    
    # Calculate the positions of the linkages
    A_x = linkage_length_A * np.cos(theta_A)
    A_y = linkage_length_A * np.sin(theta_A)
    A_z = 0

    B_x = linkage_length_B * np.cos(theta_B)
    B_y = 0
    B_z = linkage_length_B * np.sin(theta_B)

    # Update data for linkages
    line_A.set_data([0, A_x], [0, A_y])
    line_A.set_3d_properties([0, A_z])
    line_B.set_data([A_x, A_x + B_x], [A_y, A_y + B_y])
    line_B.set_3d_properties([0, B_z])
    
    return line_A, line_B,

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), init_func=init, blit=True, interval=50)

# Show the plot
plt.legend()
plt.grid()
plt.show()
