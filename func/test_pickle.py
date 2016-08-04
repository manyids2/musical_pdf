import matplotlib.pyplot as plt
import pickle
from mpl_toolkits.mplot3d import Axes3D

t_m,t_v,t_u,f_m,f_v,f_u = pickle.load( open( "save.p", "rb" ) )

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(t_m,t_v,t_u,c='r')
ax.scatter(f_m,f_v,f_u,c='b')
plt.show()