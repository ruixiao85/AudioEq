#!/usr/bin/env python
import os, sys
from util import parse_args, map_subfolder, short_name, band_side as get_freq_resp
args=parse_args("foobar31geq")
fmap=map_subfolder(args.idir, args.fext)
print(fmap) # { 'oratory1990': ['AKG K701', ...], ... }
if not fmap: sys.exit()

bands=[20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,
  1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000] # 31 Graphic Equalizer
import binascii
prehex='66 6F 6F 5F 64 73 70 5F 78 67 65 71 0D 0A 31 0D 0A 76 3A 0C E7 A7 88 9F 41 A2 EA B0 0C 3A 9A C7 42 16 01 00 00 03 00 00 00 00 00 00 00 02 00 00 00'.replace(' ','')
midhex='00 1F 00 00 00'.replace(' ','') # 4 bytes of global gain between pre and mid
posthex='00 00 00 00 01 1F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ','')

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
              # with open(os.path.join(args.out, f"{_p}-{_v}~{ratio}{limit}{k[:2]}.xgeq"), "wb") as f:
              with open(os.path.join(args.out, f"{_v}~{ratio}{limit}{k[:2]}~{_p}.xgeq"), "wb") as f:
                f.write(binascii.unhexlify(prehex))
                adjs=[(b-a)*0.1*(1+ratio) for a,b in zip(fr1,fr2)]
                mean=max(-2**limit,min(2**limit,sum(adjs)/len(adjs)))
                f.write((10*round(10*mean)).to_bytes(4,byteorder='little',signed=True))
                f.write(binascii.unhexlify(midhex))
                for adj in adjs:
                  f.write((10*round(10*max(-2**limit,min(2**limit,adj-mean)))).to_bytes(4,byteorder='little',signed=True))
                f.write(binascii.unhexlify(posthex))
            # exit(1) # debug one case
