import os
import numpy as np

path_ = '/home/mukunar1/workspace/wonderingEar/music_learn/musical_pdf/data/pdfs'
books = os.listdir( path_ )
f_ = [s for s in books if not os.path.isdir(os.path.join(path_,s))]
d_ = [s for s in books if     os.path.isdir(os.path.join(path_,s))]

books_txt = open('books.txt', 'w')
for s in d_: books_txt.write(os.path.join(path_,s)+'\n')
books_txt.close()

test_pages = open('test_pages.txt', 'w')
all_pages  = open('all_pages.txt' , 'w')
count = 0
for d in d_:
  names_txt = open('names_'+d+'.txt', 'w')
  book_ = os.path.join(path_,d)
  pages = os.listdir(book_)
  p_ = [s for s in pages if s[-4:]=='.png']
  for s in p_: names_txt.write(s+'\n')
  for s in p_: all_pages.write(os.path.join(book_,s)+'\n')
  n_ = map(int,np.random.permutation(len(p_))[:20])
  for s in n_: test_pages.write(os.path.join(book_,p_[s])+'\n')
  names_txt.close()
  count = count + len(p_)
print count
all_pages.close()
test_pages.close()