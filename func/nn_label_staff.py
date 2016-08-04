import numpy as np
import cv2
from scipy import signal
import matplotlib.pyplot as plt
import pickle
from mpl_toolkits.mplot3d import Axes3D

# Read all sections of a page
# Select page sequentially
f_in  = open('../data/temp/all_pages_train.txt','r' )
f_out = open('../data/temp/is_staff.txt'       ,'a' )
f_data= open('../data/temp/filter_data_2.bin'  ,'wb')
b    = False
c    = 0
s    = 50
l    = 100
h    = 1000
N    = (h-l)/s
fft_ = []
max_ = []
mn_  = []
var_ = []
t_m  = []
t_v  = []
t_u  = []
f_m  = []
f_v  = []
f_u  = []

for line in f_in:
  img = cv2.resize((cv2.imread(line[:-1],0)),(1000,1000))
  f_out.write('\n'+line+'h:1000,w:1000,s:50,l:100\n')
  img          = 255 - np.array(img)
  filter_staff = np.array([[-255,-255,-255,-255,-255],[255,255,255,255,255],[255,255,255,255,255],[-255,-255,-255,-255,-255]])
  grad         = signal.convolve2d(img, filter_staff, boundary='symm', mode='same')
  sum_vert     = np.sum(grad,1)
  for i in range(N):
    sec = img[i*s:i*s+l,:]
    ff = np.abs(np.fft.rfft(sum_vert[i*s:i*s+l]))
    fft_.append(np.vstack((range(len(ff)),ff)))
    max_.append(np.argmax(ff))
    mn_.append(np.mean(ff))
    var_.append(np.var(ff))
    cv2.imshow('section',sec)
    k = cv2.waitKey(0)
    if k==1048603:
      b = True
    if k==1048692:
      t_m.append(mn_[-1] )
      t_v.append(var_[-1])
      t_u.append(np.max(ff))
      f_out.write(str(i)+':1,')
    if k==1048678:
      f_m.append(mn_[-1] )
      f_v.append(var_[-1])
      f_u.append(np.max(ff))
      f_out.write(str(i)+':0,')
  if b: break
  c = c + 1
  print c, mn_[-1], var_[-1]
  if c>100:
    break

np.array(fft_).tofile(f_data)
f_data.close()
f_out.close()
f_in.close()
pickle.dump([t_m,t_v,t_u,f_m,f_v,f_u], open( "save2.p", "wb" ) )

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(t_m,t_v,t_u,color='r')
ax.scatter(f_m,f_v,f_u,color='b')
plt.show()