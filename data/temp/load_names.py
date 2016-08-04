all_pages = open('test_pages.txt', 'r')
count = 0
for line in all_pages:
  print line
  count = count + 1
all_pages.close()
print count