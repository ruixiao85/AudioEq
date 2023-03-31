#!/bin/env python
from pathlib import Path
import os
limit=12; ratios=[0.6,1.0] # with limit and scaling
# limit=99; ratios=[1.0] # raw conversion
nbands=31
bands=[20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,
  1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000] # 31 Graphic Equalizer

from util import short_name, band_left as get_freq_resp
# from util import short_name, band_int_round as get_freq_resp

def short_name(file: str)-> str:
  return file.replace("-","").replace(" ","").lower()

import binascii
prehex='66 6F 6F 5F 64 73 70 5F 78 67 65 71 0D 0A 31 0D 0A 76 3A 0C E7 A7 88 9F 41 A2 EA B0 0C 3A 9A C7 42 16 01 00 00 03 00 00 00 00 00 00 00 02 00 00 00'.replace(' ','')
midhex='00 1F 00 00 00'.replace(' ','') # 4 bytes of global gain between pre and mid
posthex='00 00 00 00 01 1F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ','')

# myHps,myHpType=["Sennheiser HD 800"],"onear"
# myHps,myHpType=["Audio-Technica ATH-W5000","Audio-Technica ATH-W5000 2013","Sennheiser HD 600", "Sennheiser HD 800","AKG K701"],"onear"
# myBrands=["Abyss","Audio-Technica","Audeze","AKG","Beyerdynamic","Dan","Denon","E-Mu","Focal","Fostex","Grado","HiFiMAN","Meze","MrSpeakers","Philips","Pioneer","Sennheiser","Sony","Stax","Ultrasone","Yamaha","ZMF"]

# myHps,myHpType=["Sennheiser IE 800"],"inear"
myHps,myHpType=["Etymotic ER2XR"],"inear"
myBrands=["Audio-Technica","Audeze","AKG","Beyerdynamic","Bose","Bowers","Denon","E-Mu","Etymotic","Focal","Fostex","Grado","HiFiMAN", "Massdrop","Meze","Monoprice","Monster","MrSpeakers","Oppo","Pioneer","Polk","Sennheiser","Shure","Sony","Stax","Tin","Ultrasone","ZMF"]

myHpsClean=[short_name(hp) for hp in myHps]

myBrandsClean=[short_name(b) for b in myBrands]
subDir="measurements"
outDir="out_eq31"
try: os.mkdir(outDir)
except OSError as e: pass
for sourceDir in ["headphonecom", "innerfidelity", "oratory1990"]:
  for dirpath,dirnames,filenames in os.walk(f"{subDir}/{sourceDir}/data/{myHpType}"):
    hpsFoundClean=[short_name(hp) for hp in dirnames]
    for hpc in myHps:
      if short_name(hpc) in hpsFoundClean:
        try: os.mkdir(f'{outDir}/{hpc}'.replace(" ","")); except OSError as e: pass
        fc=get_freq_resp(f"{subDir}/{sourceDir}/data/{myHpType}/{hpc}")
        print(fc)
        for hpt in dirnames:
          if short_name(hpt.split(" ")[0]) in myBrandsClean:
            ft=get_freq_resp(f"{subDir}/{sourceDir}/data/{myHpType}/{hpt}")
            for ratio in ratios:
              with open(f'{outDir}/{hpc}/{hpt}~{ratio}~{sourceDir}.xgeq'.replace(" ",""),"wb") as f:
                f.write(binascii.unhexlify(prehex))
                adjs=[(b-a)*ratio for a,b in zip(fc,ft)]
                mean=max(-1*limit,min(limit,sum(adjs)/len(adjs)))
                f.write((10*round(10*mean)).to_bytes(4,byteorder='little',signed=True))
                f.write(binascii.unhexlify(midhex))
                for adj in adjs:
                  f.write((10*round(10*max(-1*limit,min(limit,adj-mean)))).to_bytes(4,byteorder='little',signed=True))
                f.write(binascii.unhexlify(posthex))
                  # f.write(f'{max(-1*limit,min(limit,round((b-a)*ratio)))}\n')
            # exit(1) # debug one case
