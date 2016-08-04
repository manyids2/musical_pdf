import numpy as np
import cv2
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_line(num, data, line):
  line.set_data(data[min(num,18)])
  return line,

f     = open('../data/temp/all_pages.txt','r')
n     = np.random.randint(800)
count =  0
for line in f:
  count = count + 1
  if count>n: break
print line[:-1]

img          = cv2.resize(cv2.imread(line[:-1],0),(500,1000))
img          = 255 - np.array(img)
filter_staff = np.array([[-255,-255,-255,-255,-255],[255,255,255,255,255],[255,255,255,255,255],[-255,-255,-255,-255,-255]])
grad         = signal.convolve2d(img, filter_staff, boundary='symm', mode='same')
sum_vert     = np.sum(grad,1)
fig2 = plt.plot(range(len(sum_vert)), sum_vert)

(h,w)= img.shape
l    = 100
s    = 50
N    = (h-l)/s
fft_ = []
max_ = []
mn_  = []
var_ = []
for i in range(N):
  ff = np.abs(np.fft.rfft(sum_vert[i*s:i*s+l]))
  fft_.append(np.vstack((range(len(ff)),ff)))
  max_.append(np.argmax(ff))
  mn_.append(np.mean(ff))
  var_.append(np.var(ff))


canvas = np.zeros(img.shape)
fig1   = plt.figure()
print max_
while True:
  cv2.imshow('grad',grad)
  for j,st in enumerate(max_):
    y = [j*s+o for o in range(0,100,st)]
    canvas = img.copy()
    for y_ in y:
      cv2.line(canvas,(0,y_),(w,y_),255)
    cv2.imshow('image',canvas)
    k = cv2.waitKey(500)
  if k==1048603: break

l_, = plt.plot([], [], 'r-')
plt.xlim(0, 100)
plt.ylim(0, 1e+9)
line_ani = animation.FuncAnimation(fig1, update_line, 18, fargs=(fft_, l_),
                                   interval=500, blit=True)
plt.show()
f.close()