import numpy as np
import cv2

all_pages = open('test_pages.txt', 'r')
count = 0
for line in all_pages:
  count = count + 1
  img = cv2.resize(cv2.imread(line[:-1]),(1000,1000))
  cv2.imshow('Image',img)
  if cv2.waitKey(0)==1048603: break
all_pages.close()
print count