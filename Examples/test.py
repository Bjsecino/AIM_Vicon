from Vicon import Vicon
import math
import numpy as np
import matplotlib.pyplot as plt

file = "/home/benjamin/Desktop/Subject01_Unloaded_Bend_R00.csv"

vicon = Vicon(file)
r_knee_center = vicon.get_model_output().get_right_leg().knee.center
r_knee_angle = vicon.get_model_output().get_right_leg().knee.angle.x

markers = vicon.get_markers()
markers.smart_sort()

r_tiba = markers.get_marker("RTIBA")

r_dists = []

print r_knee_center.x[0]
print r_tiba[0].x

for idx in range(len(r_tiba)):
    r_dist = math.sqrt(math.pow(r_knee_center.x[idx] - r_tiba[idx].x, 2) + math.pow(r_knee_center.y[idx] - r_tiba[idx].y, 2) + math.pow(r_knee_center.z[idx] - r_tiba[idx].z, 2))
    r_dists.append(r_dist)

r_dist_offset = sorted(r_dists)[0]
r_ang_offset = sorted(r_knee_angle)[0]

r_ang_dist = []

for idx in range(len(r_dists)):
    r_ang_dist.append([r_knee_angle[idx] - r_ang_offset, r_dists[idx] - r_dist_offset])

r_sorted = sorted(r_ang_dist, key=lambda  x: x[0])

R_sorted = np.array(r_sorted)

plt.figure(1)
plt.plot(r_dists)
plt.xlabel('frame')
plt.ylabel('displacement')
plt.title('Right Knee Displacement vs Frame')


plt.figure(2)
plt.scatter(R_sorted[:, 0], R_sorted[:, 1])
plt.xlabel('angle')
plt.ylabel('displacement')
plt.title('Right Knee Angle vs Displacement')


plt.figure(3)
plt.plot(r_knee_angle)
plt.xlabel('frame')
plt.ylabel('angle')
plt.title('Right Knee Angle vs Frame')


plt.show()