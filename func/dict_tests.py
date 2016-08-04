import pickle

def getNames():
  path = '/home/mukunar1/workspace/wonderingEar/music_learn/musical_pdf/data/pdfs/'
  books = dict()
  f = open('../data/temp/all_pages.txt','r')
  for line in f:
    l_ = line.split('/')
    if not l_[-2] in books: books[l_[-2]] = []
    books[l_[-2]].append(l_[-1][:-1])
  f.close()
  return path,books

[path,books] = getNames()
b = books.keys()
print path+b[0]+'/'+books[b[0]][0]