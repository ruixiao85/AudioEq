#!/usr/bin/env python
import os, sys
from util import parse_args, map_subfolder, short_name, band_side as get_freq_resp
args=parse_args("wavelet")
fmap=map_subfolder(args.idir, args.fext)
print(fmap) # { 'oratory1990': ['AKG K701', ...], ... }
if not fmap: sys.exit()
os.makedirs(args.out, exist_ok=True)

bands=[20, 21, 22, 23, 24, 26, 27, 29, 30, 32, 34, 36, 38, 40, 43, 45, 48, 50, 53, 56, 59, 63, 66, 70, 74, 78, 83, 87, 92, 97, 103, 109, 115, 121, 128, 136, 143, 151, 160, 169, 178, 188, 199, 210, 222, 235, 248, 262, 277, 292, 309, 326, 345, 364, 385, 406, 429, 453, 479, 506, 534, 565, 596, 630, 665, 703, 743, 784, 829, 875, 924, 977, 1032, 1090, 1151, 1216, 1284, 1357, 1433, 1514, 1599, 1689, 1784, 1885, 1991, 2103, 2221, 2347, 2479, 2618, 2766, 2921, 3086, 3260, 3443, 3637, 3842, 4058, 4287, 4528, 4783, 5052, 5337, 5637, 5955, 6290, 6644, 7018, 7414, 7831, 8272, 8738, 9230, 9749, 10298, 10878, 11490, 12137, 12821, 13543, 14305, 15110, 15961, 16860, 17809, 18812, 19871]

for p in args.fr: # headPhone to start from
  for k, vs in fmap.items(): # key: data source, values: list of headphone data points
    if p in vs:
      print(f"found {p} in {k}"); _p=short_name(p)
      fr1=get_freq_resp(f"{args.idir}/{k}/{p}{args.fext}", bands)
      for v in vs:
        if v!=p and (not args.to or v in args.to): # targeting a different headphone
          print(f"targeting {v}"); _v=short_name(v)
          fr2=get_freq_resp(f"{args.idir}/{k}/{v}{args.fext}", bands)
          for ratio in args.ratio:
            for limit in args.limit:
              # print(f"ratio {ratio} limit {limit}")
              with open(os.path.join(args.out, f"{_p}-{_v}~{ratio}{limit}{k[:2]}.txt"), "w") as f:
                f.write("GraphicEQ: ")
                adjs=[(b-a)*0.1*(1+ratio) for a,b in zip(fr1,fr2)]
                mean=max(-2**limit,min(2**limit,sum(adjs)/len(adjs))); # mean=0
                for band,adj in zip(bands, adjs):
                  # print(f"band {band}")
                  f.write(f"{band} {round(max(-2**limit,min(2**limit,adj-mean)),2)}; ")

