#Post processing file
import numpy as np
import matplotlib.pyplot as plt
import Action_file as act
from mpl_toolkits.mplot3d import Axes3D


#Og_coor
og_coor = act.Nodecoor[: , :]
New_coor = act.N_disp[: , :]

#Plotting the original and new coordinates
fig = plt.figure
fig.suptitle('Original and New Coordinates')

ax = fig.addsubplot(111, projection='3d')

ax.plot(og_coor[:, 0], og_coor[:, 1], og_coor[:, 2], 'r')
ax.plot(New_coor[:, 0], New_coor[:, 1], New_coor[:, 2], 'r')

plt.show()

