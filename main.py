import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading, time
from inv_kin_calculate import inv_kin

# Set up the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title('2D Manipulator Arm')

# Set up the arm
arm, = ax.plot([0, 1], [0, 0], 'r-', lw=5)
elbow, = ax.plot([1, 2], [0, 0], 'b', lw=5)
elbow2, = ax.plot([2, 3], [0, 0], 'g', lw=5)
angles = [10, 15, 20]


def draw_arm(length, angle1, angle2, angle3):
    x = length * np.cos(np.radians(angle1))
    y = length * np.sin(np.radians(angle1))
    arm.set_xdata([0, x])
    arm.set_ydata([0, y])
    x2 = x + length * np.cos(np.radians(angle1 + angle2))
    y2 = y + length * np.sin(np.radians(angle1 + angle2))
    elbow.set_xdata([x, x2])
    elbow.set_ydata([y, y2])
    x3 = x2 + length * np.cos(np.radians(angle1 + angle2 + angle3))
    y3 = y2 + length * np.sin(np.radians(angle1 + angle2 + angle3))
    elbow2.set_xdata([x2, x3])
    elbow2.set_ydata([y2, y3])
    fig.canvas.draw_idle()


def animate(i, angles):
    angle1 = angles[0]
    angle2 = angles[1]
    angle3 = angles[2]
    length = 1
    draw_arm(length, angle1, angle2, angle3)
    
    
def angle_update():
    while True:
        x1, x2 = input('Enter x1, x2: ').split()
        x1 = float(x1)
        x2 = float(x2)
        angle1, angle2, angle3 = inv_kin(x1, x2, angles[0], angles[1], angles[2])
        
        angle1 = float(angle1)%360
        angle2 = float(angle2)%360
        angle3 = float(angle3)%360
        
        print(angle1, angle2, angle3)
        
        if(angle1 > 180):
            angle1 = angle1 - 360
        if(angle2 > 180):
            angle2 = angle2 - 360
        if(angle3 > 180):
            angle3 = angle3 - 360
        
        # animate from angles[0] to angle1 and angles[1] to angle2
        delta1 = (angle1 - angles[0])/100
        delta2 = (angle2 - angles[1])/100
        delta3 = (angle3 - angles[2])/100
        
        for i in range(100):
            angles[0] = angles[0] + delta1
            angles[1] = angles[1] + delta2
            angles[2] = angles[2] + delta3
            time.sleep(0.01)
    
    
threading.Thread(target=angle_update).start()

ani = animation.FuncAnimation(fig, animate, frames=100, fargs=[angles,], interval=100) 


plt.show()

