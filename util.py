import os, sys
from collections import OrderedDict

def parse_args(use:str="equalizer"):
  import argparse
  from datetime import datetime
  parser = argparse.ArgumentParser(f"Generate eq profiles for {use}.")
  parser.add_argument("-f", "--fr", default=[], type=str, help="adjust eq from which earphone(s).", action='append')
  parser.add_argument("-t", "--to", default=[], type=str, help="adjust eq to which earphone(s). Default to all available earphones.", action='append')
  parser.add_argument("-r", "--ratio", default=[], type=int, help="degree of eq adjustments, ratio: 0 - 9. 9=100% adj", action='append')
  parser.add_argument("-l", "--limit", default=[], type=int, help="degree of eq adjustments, limit: 0 - 5. 4=2^4= +/-16db", action='append')
  parser.add_argument("-i", "--idir", default="db", type=str, help="database root directory path")
  parser.add_argument("-e", "--fext", default=".csv", type=str, help="eq raw data file extension")
  parser.add_argument("-u", "--use", default=use, type=str, help="detailed use case of the eq adjustments.")
  parser.add_argument("-o", "--out", default="_".join([use, datetime.now().strftime("%y%m%dT%H%M")]), type=str, help="detailed use case of the eq adjustments.")
  args=parser.parse_args()
  if not args.fr: sys.exit("from earphone(s) required! e.g., -f \"AKG K701\"")
  # args.fr=["AKG K701"] # use a default
  if not args.ratio: args.ratio=[9]
  if not args.limit: args.limit=[4]
  if not args.out.startswith("out/"): args.out=os.path.join("out", args.out) # force nest under out/
  print(args)
  return args

def map_subfolder(root, ext):
  fmap={}
  for sub in os.listdir(root):
    if os.path.isdir(os.path.join(root, sub)):
      # print(sub)
      lst=[f.replace(ext,"") for f in os.listdir(os.path.join(root, sub)) if f.endswith(ext)]
      fmap[sub]=lst
  return fmap

def short_name(file: str)-> str:
  res=file
  for w in ["-", " "]:
    res=res.replace(w, "")
  for f,t in [ ("AnkerSoundcore", "Akr"), ("AudioTechnica", ""), ("Audeze", "Adz"),
    ("Beyerdynamic", "Byr"),
    ("Sennheiser", "Sen"), ("Bowers&Wilkins", "B&W"), ("Bang&Olufsen", "B&O"),
    ("CampfireAudio", "Campf"), ("DanClarkAudio", "Dan"),
    ("Edition", "Ed"), ("Etymotic", "Ety"),
    ("HIFIMAN", "Hfm"), ("Moondrop", "Mdp"),
    ("Shure", "Shu"), ("Tin HiFi", "Tin"),
    ("Vision Ears", "Vse"), ("Ultrasone", "Uts"),
  ]:
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
