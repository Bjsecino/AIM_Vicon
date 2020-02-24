from Vicon import Vicon
import numpy as np
import math
from Session import ViconGaitingTrial as Trial
import matplotlib.pyplot as plt


file = "/home/benjamin/Desktop/Subject01_Unloaded_Bend_R00.csv"

vicon = Vicon(file)
l_knee_center = vicon.get_model_output().get_right_leg().knee.center


#file = "/home/benjamin/Desktop/Subject Data/Subject00/12162019/Subject00_Loaded_Bend_00.csv"

# Extract joint angles
trial = Trial.ViconGaitingTrial(vicon_file=file)

r_joints = trial.vicon.get_model_output().get_right_leg()
#l_joints = trial.vicon.get_model_output().get_left_leg()

r_knee = r_joints.knee

r_angles = r_joints.knee.angle.x
#l_angles = l_joints.knee.angle.x


# Extract distances
data = Vicon.Vicon(file)
markers = data.get_markers()
markers.smart_sort()
#markers.auto_make_frames()
r_knee_inner = markers.get_marker("R_Knee_Inner")
#l_knee_inner = markers.get_marker("L_Knee_Inner")
r_knee_outer = markers.get_marker("RKNE")
#l_knee_outer = markers.get_marker("LKNE")
r_tiba = markers.get_marker("RTIBA")
#l_tiba = markers.get_marker("LTIBA")

#submit issues: auto_make_frames sucks, auto fill empty cells with zeros

r_dists = []
#l_dists = []

for idx in range(len(r_knee_inner)):
#for idx in range(200):

    r_knee_center_x = (r_knee_inner[idx].x + r_knee_outer[idx].x) / 2.0
    r_knee_center_y = (r_knee_inner[idx].y + r_knee_outer[idx].y) / 2.0
    r_knee_center_z = (r_knee_inner[idx].z + r_knee_outer[idx].z) / 2.0

    #l_knee_center_x = (l_knee_inner[idx].x + l_knee_outer[idx].x) / 2.0
    #l_knee_center_y = (l_knee_inner[idx].y + l_knee_outer[idx].y) / 2.0
    #l_knee_center_z = (l_knee_inner[idx].z + l_knee_outer[idx].z) / 2.0

    r_dist = math.sqrt(math.pow(r_knee_center_x - r_tiba[idx].x, 2) + math.pow(r_knee_center_y - r_tiba[idx].y, 2) + math.pow(r_knee_center_z - r_tiba[idx].z, 2))
    #l_dist = math.sqrt(math.pow(l_knee_center_x - l_tiba[idx].x, 2) + math.pow(l_knee_center_y - l_tiba[idx].y, 2) + math.pow(l_knee_center_z - l_tiba[idx].z, 2))

    r_dists.append(r_dist)
    #l_dists.append(l_dist)

# find offsets
r_dist_offset = sorted(r_dists)[0]
#l_dist_offset = sorted(l_dists)[0]

r_ang_offset = sorted(r_angles)[0]
#l_ang_offset = sorted(l_angles)[0]

# Combine angles and distances
r_ang_dist = []
#l_ang_dist = []

for idx in range(len(r_dists)):
    r_ang_dist.append([r_angles[idx] - r_ang_offset, r_dists[idx] - r_dist_offset])
    #l_ang_dist.append([l_angles[idx] - l_ang_offset, l_dists[idx] - l_dist_offset])

# Sort by angle
r_sorted = sorted(r_ang_dist, key=lambda x: x[0])
#l_sorted = sorted(l_ang_dist, key=lambda x: x[0])

# Plotting
R_sorted = np.array(r_sorted)
#L_sorted = np.array(l_sorted)

plt.figure(1)
plt.plot(r_dists)
plt.xlabel('frame')
plt.ylabel('displacement')
plt.title('Right Knee Displacement vs Frame')


num = file[-5]
plt.figure(num)
plt.scatter(R_sorted[:, 0], R_sorted[:, 1])
plt.xlabel('angle')
plt.ylabel('displacement')
plt.title('Right Knee Angle vs Displacement')

#plt.figure(3)
#plt.scatter(L_sorted[:, 0], L_sorted[:, 1])
#plt.xlabel('angle')
#plt.ylabel('displacement')
#plt.title('Left Knee Angle vs Displacement')
plt.show()