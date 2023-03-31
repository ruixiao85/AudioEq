#!/bin/env python
from pathlib import Path
import os
bands=[55,77,110,156,220,311,440,622,880,1200,1800,2500,3500,5000,7000,10000,14000,20000]
limit=20

from util import short_name, band_left as get_freq_resp

myHps=["Audio-Technica ATH-W5000","Sennheiser HD 600", "Sennheiser HD 800","AKG K701"]
myHpsClean=[short_name(hp) for hp in myHps]
myBrands=["Audio-Technica","Audeze","AKG","Beyerdynamic","Bose","Bowers","Denon","E-Mu","Focal","Fostex","Grado","HiFiMAN",
  "Massdrop","Meze","Monoprice","Monster","MrSpeakers","Oppo","Pioneer","Polk","Sennheiser","Shure","Sony","Stax","Ultrasone","ZMF"]
myBrandsClean=[short_name(b) for b in myBrands]
for sourceDir in ["headphonecom", "innerfidelity", "oratory1990"]:
  for dirpath,dirnames,filenames in os.walk(f"{sourceDir}/data/onear"):
    hpsFoundClean=[short_name(hp) for hp in dirnames]
    for hpc in myHps:
      if short_name(hpc) in hpsFoundClean:
        try: os.mkdir(f'{sourceDir}~{hpc}'.replace(" ",""))
        except OSError as e: pass
        fc=get_freq_resp(f"{sourceDir}/data/onear/{hpc}")
        print(fc)
        for hpt in dirnames:
          if clean_name(hpt.split(" ")[0]) in myBrandsClean and clean_name(hpt) not in myHpsClean:
            ft=get_freq_resp(f"{sourceDir}/data/onear/{hpt}")
            for ratio in [0.6,1.0]:
              with open(f'{sourceDir}~{hpc}/{hpt}~{ratio}.feq'.replace(" ",""),"w") as f:
                for a,b in zip(fc,ft):
                  f.write(f'{max(-1*limit,min(limit,round((b-a)*ratio)))}\n')

