#!/usr/bin/env python
import os, sys
from util import parse_args, map_subfolder, short_name, band_side as get_freq_resp
args=parse_args("foobar18eq")
fmap=map_subfolder(args.idir, args.fext)
print(fmap) # { 'oratory1990': ['AKG K701', ...], ... }
if not fmap: sys.exit()

bands=[55,77,110,156,220,311,440,622,880,1200,1800,2500,3500,5000,7000,10000,14000,20000]

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
              # with open(os.path.join(args.out, f"{_p}-{_v}~{ratio}{limit}{k[:2]}.feq"), "w") as f:
              with open(os.path.join(args.out, f"{_v}~{ratio}{limit}{k[:2]}~{_p}.feq"), "w") as f:
                adjs=[(b-a)*0.1*(1+ratio) for a,b in zip(fr1,fr2)]
                mean=max(-2**limit,min(2**limit,sum(adjs)/len(adjs))); # mean=0
                for band,adj in zip(bands, adjs):
                  # print(f"band {band}")
                  f.write(f"{round(max(-2**limit,min(2**limit,adj-mean)),2)}\n")

