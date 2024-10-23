import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Create a figure for the mechanism sketch
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Initial positions
pivot_x = 1
pivot_y = 2
screw_x = [1.5, 1.5]
screw_y = [0, 4]
follower_x = 2.5  # Follower's x position remains constant
linkage1_x = [1.5, pivot_x]
linkage2_x = [pivot_x, follower_x]

# Draw initial components
pivot_point, = ax.plot([pivot_x], [pivot_y], [0], 'ko', markersize=8)  # Pivot point
screw_line, = ax.plot(screw_x, screw_y, [0, 0], 'b-', lw=4)  # Ball screw (3D)
follower_line, = ax.plot([follower_x, follower_x], [2, 2], [0, 0], 'r-', lw=4)  # Follower (3D)
linkage1_line, = ax.plot(linkage1_x, [2, pivot_y], [0, 0], 'g-', lw=2)  # Linkage 1
linkage2_line, = ax.plot(linkage2_x, [pivot_y, 2], [0, 0], 'g-', lw=2)  # Linkage 2

# Set limits and labels
ax.set_xlim(0, 3.5)
ax.set_ylim(-0.5, 4.5)
ax.set_zlim(-1, 1)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('3D Animated Flexible Linkage Mechanism for Ball Screw Follower')
ax.view_init(elev=20, azim=30)  # Set the view angle
ax.grid()

# Function to update the animation
def update(frame):
    # Determine the angle of rotation (0 to 90 degrees)
    angle = np.radians(frame * 90 / 100)  # Rotate from 0 to 90 degrees
    # Rotation around the screw (1.5, y) where y is the follower's height
    follower_y_rotated = pivot_y + np.sin(angle)  # Circular motion
    follower_z_rotated = np.cos(angle)  # Movement along z-axis

    # Update follower's position in 3D
    follower_line.set_data([follower_x, follower_x], [follower_y_rotated, follower_y_rotated])
    follower_line.set_3d_properties([follower_z_rotated, follower_z_rotated])

    # Update linkages based on the pivot and follower position
    linkage1_line.set_ydata([2, pivot_y])  # Linkage 1 stays fixed
    linkage2_line.set_data([pivot_x, follower_x], [pivot_y, follower_y_rotated])  # Update linkage to follower
    linkage2_line.set_3d_properties([0, follower_z_rotated])  # Update z for linkage 2

    # After reaching the peak, translate follower vertically
    if frame >= 100:  # Start translation after the rotation is done
        translation_frame = frame - 100  # Offset for translation frames
        translation_height = 4 * (translation_frame / 100)  # Move from 0 to 4
        follower_line.set_data([follower_x, follower_x], [translation_height, translation_height])
        follower_line.set_3d_properties([0, 0])
        linkage2_line.set_data([pivot_x, follower_x], [pivot_y, translation_height])  # Update linkage to new follower position
        linkage2_line.set_3d_properties([0, 0])  # Keep z constant during translation

    return pivot_point, screw_line, follower_line, linkage1_line, linkage2_line

# Create animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 200), blit=True, interval=100)

# Show the animation
plt.show()
