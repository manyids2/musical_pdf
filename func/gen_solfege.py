import numpy as np
import pickle
import re

def dist(e1,e2):
  print e1,e2

class params:
  def __init__(self):
    self.ps0 = np.zeros((7,1))
    self.tm  = np.zeros((7,7))

class chain:
  def __init__(self,N):
    self.K      = 7
    self.N      = N
    self.notes  = ['c','d','e','f','g','a','b','c','d','e','f','g','a','b','c','d','e','f','a','b','g','r','l']
    self.states = range(self.K)
    self.seq    = [node(i) for i in range(N)]
    self.tm     = np.zeros((self.K,self.K))
    self.ps0    = np.zeros((self.K,1     ))

    self.octave_maps = dict()
    self.octave_maps['c'] = [ 0, 0, 0, 0,-1,-1,-1]
    self.octave_maps['d'] = [ 0, 0, 0, 0, 0,-1,-1]
    self.octave_maps['e'] = [ 0, 0, 0, 0, 0, 0,-1]
    self.octave_maps['f'] = [ 0, 0, 0, 0, 0, 0, 0]
    self.octave_maps['g'] = [+1, 0, 0, 0, 0, 0, 0]
    self.octave_maps['a'] = [+1,+1, 0, 0, 0, 0, 0]
    self.octave_maps['b'] = [+1,+1,+1, 0, 0, 0, 0]

  def set_state(self,n,k):
    self.seq[n].state = k

  def set_transition_matrix(self,P):
    self.tm = P

  def set_prob_s0(self,p):
    self.ps0 = p

  def print_chain(self):
    s = 'c\'2 c | '
    n = self.notes[self.seq[0].emit]
    if self.octave_maps['c'][self.seq[0].emit]==1:
      s = s+n+',4 '
    if self.octave_maps['c'][self.seq[0].emit]==-1:
      s = s+n+'\'4 '
    if self.octave_maps['c'][self.seq[0].emit]==0:
      s = s+n+'4 '
    octave = 0
    for i in range(7):
      o = self.notes[self.seq[i  ].emit]
      n = self.notes[self.seq[i+1].emit]
      if self.octave_maps[o][self.seq[i+1].emit]==+1:
        s = s+n+', '
      if self.octave_maps[o][self.seq[i+1].emit]==-1:
        s = s+n+'\' '
      if self.octave_maps[o][self.seq[i+1].emit]==0:
        s = s+n+' '
      if (i+2)%4==0:
        s = s+'| '
    return s

  def set_params(self,params_file):
    params_f = open(params_file, 'rb')
    p = params()
    p = pickle.load(params_f)
    self.set_prob_s0(p.ps0)
    self.set_transition_matrix(p.tm)

  def draw(self,p):
    d = np.random.uniform()
    cdf = [np.sum(p[0:k]) for k in range(self.K)]
    cdf.append(1)
    for k in range(self.K):
      if (d>cdf[k])&(d<cdf[k+1]):
        return k

  def gen_chain(self):
    self.seq[0].state = self.draw(self.ps0)
    for i in range(self.N-1):
      self.seq[i+1].state = self.draw(self.tm[self.seq[i].state])
    for i in range(self.N):
      self.seq[i].emit = self.map(self.seq[i].state)

  def map(self,i):
    if i==0: return 1-1
    if i==1: return 3-1
    if i==2: return 5-1
    if i==3: return 2-1
    if i==4: return 4-1
    if i==5: return 6-1
    if i==6: return 7-1

class node:
  def __init__(self,n):
    self.emit  = 9
    self.state = 0

class Quest:
  def __init__(self,name):
    self.name  = name
    self.tempo = (120,4)
    self.bpts  = '4/4, 8/4'
    self.time  = (4,4)
    self.key   = 'c \\major'
    self.notes = 'c\'4 [d8 e8] | f4. [f16 g] | [a8 a] [c a] | [a g] r c |'
    self.c     = chain(8)

  def get_notes(self,lesson):
    if lesson==1:
      params_file = 'params_file_123.p'
      self.c.set_params(params_file)
      self.c.gen_chain()
    return self.c.print_chain()

  def get_string(self,notes):
    self.notes = notes
    t_head     = 'question {\n'
    t_tail     = '}\n\n'
    t_name     = '  name = "%s"\n'
    t_tempo    = '  tempo = %d/%d\n'
    t_bpts     = '  breakpoints = %s\n'
    t_music    = '  music = rvoice("""\n'
    t_time     = '    \\time %d/%d\n'
    t_key      = '    \\key %s\n'
    t_notes    = '    %s\n'
    t_mtail    = '  """)\n'
    s = t_head             + \
        t_name%self.name   + \
        t_tempo%self.tempo + \
        t_bpts%self.bpts   + \
        t_music            + \
        t_time%self.time   + \
        t_key%self.key     + \
        t_notes%self.notes + \
        t_mtail            + \
        t_tail
    return s

def get_header():
  s = 'header {                    \n \
        module = dictation         \n \
        title = "123"              \n \
        version = "3.19.7"         \n \
      }\n\n'

  s0 = 'question {                         \n   \
        name = "Orient"                    \n   \
        tempo = 120/4                      \n   \
        breakpoints = 4/4, 8/4, 12/4, 16/4 \n   \
        music = rvoice("""                 \n   \
          \\time 4/4                       \n   \
          \key c \major                    \n   \
          c\'2 c | c4 e c g\' | c, e g c | \n   \
          c2 c | c4 e c g\' | c, e g c |   \n   \
        """)                               \n   \
      }\n\n'

  s1 = 'question {                         \n   \
        name = "Scale"                     \n   \
        tempo = 120/4                      \n   \
        breakpoints = 4/4, 8/4, 12/4, 16/4 \n   \
        music = rvoice("""                 \n   \
          \\time 4/4                       \n   \
          \key c \major                    \n   \
          c2 c | c d e f | g a b c |       \n   \
          c2 c | c d e f | g a b c |       \n   \
        """)                               \n   \
      }\n\n'

  return s+s0+s1



def print_template(name):
  s = Quest(name)
  return s.get_string(s.get_notes(1))

f = open('/home/mukunar1/.solfege/exercises/user/lesson-files/lesson_123', 'w')
f.write(get_header())
print get_header()
for i in range(30):
  score = print_template('Chain %d'%i)
  print score
  f.write(score)
f.close()
