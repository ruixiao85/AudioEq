import os
from collections import OrderedDict

def short_name(file: str)-> str:
  res=file
  for w in ["-", " ", "AudioTechnica"]:
    res=res.replace(w, "")
  for f,t in [("Sennheiser", "Senn"), ("Beyerdynamic", "Beyer"), ("DanClarkAudio", "DanClark"),
    ("Bang&Olufsen", "BnO"), ("AnkerSoundcore", "Anker")]:
    res=res.replace(f, t)
  return res

import math
def band_side(file: str, bands:list, fext: str=".csv")-> []:
  fl,vl=0,0 # last frequency and value
  bi=0; ad=[0]*len(bands) # adjustment list
  with open(file) as f:
    for li,line in enumerate(f):
      if li==0: continue # skip 1st row
      cols=line.split(',')
      fc=float(cols[0]) # frequency current
      vc=float(cols[1]) # value current
      # print(f"row {li}, f {fc}, v {vc}, bi {bi}, ft {bands[bi]}")
      if bands[bi]<=fc:
        if 2*math.log(bands[bi]+1)>math.log(fc+1)+math.log(fl+1): # gap before > after
          ad[bi]=vc
        else:
          ad[bi]=vl
        bi+=1
        if bi>=len(bands):
          break
      fl=fc; vl=vc
  # print(bands); print(ad); print(len(bands),len(ad))
  return ad
