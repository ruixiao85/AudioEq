#!/bin/env python
from pathlib import Path
import os, sys
limit=12; ratios=[0.6,0.9] # with limit and scaling
# limit=99; ratios=[1.0] # raw conversion
fext=".csv"

pretext="GraphicEQ: "
bands=[20, 21, 22, 23, 24, 26, 27, 29, 30, 32, 34, 36, 38, 40, 43, 45, 48, 50, 53, 56, 59, 63, 66, 70, 74, 78, 83, 87, 92, 97, 103, 109, 115, 121, 128, 136, 143, 151, 160, 169, 178, 188, 199, 210, 222, 235, 248, 262, 277, 292, 309, 326, 345, 364, 385, 406, 429, 453, 479, 506, 534, 565, 596, 630, 665, 703, 743, 784, 829, 875, 924, 977, 1032, 1090, 1151, 1216, 1284, 1357, 1433, 1514, 1599, 1689, 1784, 1885, 1991, 2103, 2221, 2347, 2479, 2618, 2766, 2921, 3086, 3260, 3443, 3637, 3842, 4058, 4287, 4528, 4783, 5052, 5337, 5637, 5955, 6290, 6644, 7018, 7414, 7831, 8272, 8738, 9230, 9749, 10298, 10878, 11490, 12137, 12821, 13543, 14305, 15110, 15961, 16860, 17809, 18812, 19871]
nband=len(bands)

from util import short_name, band_side as get_freq_resp

# ps=["Sennheiser HD 800"] # head/ear-phones
ps=["Sennheiser HD 800", "Audio-Technica ATH-W5000 2013", "Audio-Technica ATH-W5000", "Anker Soundcore Space Q45", "Sennheiser IE 900 RX"] # head/ear-phones
idir="db"
odir="out_wavelet"
fmap={}
for sub in os.listdir(idir):
  if os.path.isdir(os.path.join(idir, sub)):
    print(sub)
    lst=[f.replace(fext,"") for f in os.listdir(os.path.join(idir, sub)) if f.endswith(fext)]
    fmap[sub]=lst

# print(fmap) # { 'oratory1990': ['AKG K701', ...], ... }
if not fmap: sys.exit()

os.makedirs(odir, exist_ok=True)

for p in ps: # headPhone to start from
  for k, vs in fmap.items(): # key: data source, values: list of headphone data points
    if p in vs:
      print(f"found {p} in {k}"); _p=short_name(p)
      fr1=get_freq_resp(f"{idir}/{k}/{p}{fext}", bands)
      for v in vs:
        if v!=p: # targeting a different headphone
          print(f"targeting {v}"); _v=short_name(v)
          fr2=get_freq_resp(f"{idir}/{k}/{v}{fext}", bands)
          for ratio in ratios:
            # print(f"ratio {ratio}")
            with open(os.path.join(odir, f"{_p}-{_v}~{round(ratio*10)}~{k[:2]}.txt"), "w") as f:
              f.write(pretext)
              adjs=[(b-a)*ratio for a,b in zip(fr1,fr2)]
              mean=max(-1*limit,min(limit,sum(adjs)/len(adjs)))
              for band,adj in zip(bands,adjs):
                # print(f"band {band}")
                f.write(f"{band} {round(max(-1*limit,min(limit,adj-mean)),2)}; ")


